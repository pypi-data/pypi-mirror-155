"""
Pre-shared key-based certificate authority and requestor

This package implements a protocol for certificate issuance that two parties
(a server, the CA -- and a client, the requestor) can use to negotiate the
issuance of certificates valid from the perspective of the CA.  The only
prerequisites for a successful certificate issuance are:

1. There is a cleartext communication channel between the two parties.
2. Both parties already have a PSK they both trust (generated, perhaps
   with the blindecdh Python module, and then subsequently verified
   by both parties).

The purpose of this is to establish enduring trust between server and client.

After successful untampered and verified key exchange between two parties
(the server and the client), both have a shared secret they can use to encrypt
and decrypt traffic.  This is useful, but the key is not enough — the modern
goal of communications cryptography is to arrive at mutually authenticated TLS
between the peers, so that the peers can then continue in a fully symmetrically
authenticated manner (e.g. via mTLS or gRPC).

Steps:

1. The server loads or creates a CA root certificate.
2. The server instantiates an instance of CA, with the certificate.
   We supply a function create_certificate_and_key(common_name, ca=True)
   to generate CA certificates, but you can roll your own.
3. The server is informed of the incoming client's PSK via
   add_psk(client_id, PSK), where the client ID is a string either known
   beforehand or mutually agreed-upon.
4. The client instantiates an instance of Requestor, with the PSK.
5. The client creates a certificate signing request.
   We supply a function create_certificate_signing_request(cn), but you
   can roll your own.
5. The client calls Requestor.encode_csr() with the CSR, which returns
   an encrypted payload that only the server should be able to decrypt.
6. The client transmits in cleartext the payload of the request to
   the server.  The payload is safe since it's encrypted with the PSK.
7. The server receives the payload, and calls CA.issue_certificate()
   in turn, with the client ID and the payload as parameters.
   * If successful, the exchange will return a tuple of encrypted
     client certificate ready to use, and the root certificate that
     the client must use to authenticate the server.
   * If add_psk() was never called, the server will raise an exception
     UnknownRequestor() to signal that the requestor is unknown.
   * If add_psk() was called but with a PSK = None, the server will
     raise an exception Pending() to signal that the requestor is
     known, but its PSK is not known yet.
   * If decryption of the payload fails, CannotDecrypt() is raised,
     signaling that the requestor does not have the correct PSK, or
     that communications have been tampered.
8. Upon successful issue_certificate(), the server must return the two
   payloads back to the client in cleartext form.  This payload is safe
   since it's encrypted with the PSK.
9. The client recieves the payload, and calls Requestor.decode_reply(),
   with the encrypted client certificate and encrypted root certificate.
   * If successful, the ready-to-use client certificate, as well as the
     root of trust CA certificate, will be returned.
   * If communications have been tampered, or the server is malicious and
     encrypted the payloads with the wrong key, CannotDecrypt() will be
     raised instead.

Once this process is complete, the client has a client certificate properly-
signed by the server, so the client may connect to the server and the server
can identify it.  The client also has the server's public certificate, so the
client can identify the server.  This makes mutually-authenticated TLS work.
Thus, any server using the CA certificate (or, presumably, a server
certificate signed by it) can begin serving the client via TLS.  The client,
now in possession of both the server root of trust certificate, and its own
valid certificate, may connect to the server via TLS.  The server can demand
that the client present its client certificate, and reject access if the
client does not present it.  The server does not need to keep a copy of
the client certificates issued (although it may), because validity is tied
to the fact that the certificate presented by the client is signed by the
mutual root of trust.
"""


__version__ = "0.1.1"

from pskca.ca import CA
from pskca.requestor import Requestor
from pskca.ca import Pending, CannotDecrypt, UnknownRequestor
from pskca.certs import (
    create_certificate_and_key,
    create_certificate_signing_request,
    issue_certificate,
)
from pskca.types import (
    EncryptedCertificateRequest,
    EncryptedClientCertificate,
    EncryptedRootCertificate,
)

__all__ = [
    x.__name__  # type: ignore
    for x in [
        Pending,
        CannotDecrypt,
        UnknownRequestor,
        EncryptedCertificateRequest,
        EncryptedClientCertificate,
        EncryptedRootCertificate,
        CA,
        Requestor,
        create_certificate_and_key,
        create_certificate_signing_request,
        issue_certificate,
    ]
]


def __test() -> None:
    import os

    client_id = "xxx"
    ca_cert, ca_key = create_certificate_and_key(ca=True)
    client_csr, client_key = create_certificate_signing_request()
    psk = os.urandom(32)

    C = CA(ca_cert, ca_key)
    C.add_psk(client_id, psk)
    R = Requestor(psk)
    payload = R.encode_csr(client_csr)
    enc_client_cert, enc_server_cert = C.issue_certificate(client_id, payload)
    client_cert, server_cert = R.decode_reply(enc_client_cert, enc_server_cert)

    print("Client certificate obtained: %s" % client_cert)
    print("Root of trust certificate obtained: %s" % server_cert)
    print("CA certificate should match root of trust: %s" % ca_cert)


if __name__ == "__main__":
    __test()
