from typing import Tuple, Optional

from pskca.types import (
    EncryptedCertificateRequest,
    EncryptedClientCertificate,
    EncryptedRootCertificate,
    check_psk,
)
from pskca.util import TimedDict
from pskca.certs import issue_certificate

from cryptography.exceptions import InvalidKey, InvalidSignature, InvalidTag
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import (
    Certificate,
)


class Pending(Exception):
    """
    The CA knowns about the requestor, but has no PSK for it, in expectation
    that the PSK for the requestor will be added later by another process.
    """


class CannotDecrypt(Exception):
    """
    The CA knows about the requestor and its PSK, but could not decrypt the
    request from the requestor.
    """


class UnknownRequestor(Exception):
    """The requestor is not known to the CA."""


class CA:
    """
    The CA issues certificates to requestors which possess an authorized
    pre-shared key.
    """

    def __init__(
        self,
        ca_certificate: Certificate,
        ca_certificate_key: rsa.RSAPrivateKey,
        time_limit: int = 60,
        max_simultaneous_authorizations: int = 4,
    ):
        """
        Initializes the certificate authority.

        Parameters:
            ca_certificate: a Certificate object that will be sent to
            successfully-authenticated requestors as the certificate root of
            trust they must use to connect to authenticated services.  In
            short -- requestors to whom this CA issues certificates must use
            this certificate as their root of trust.
            ca_certificate_key: an RSAPrivateKey object that will be used
            to sign certificates that authenticated requestors present for
            signature.
            time_limit: defaults to 60 seconds.  Any PSK added to the CA
            will stop being valid after this time.  This is a convenient
            security feature that allows PSK authorizations to be constrained
            in duration.
            max_simultaneous_authorizations: defaults to 4.  If more than this
            number of PSKs are added, older ones will be purged.  This is
            a convenient security feature that prevents resource exhaustion
            by malicious attackers (e.g. calling code is influenced, perhaps
            by oversight, to add a large number of PSKs to this object).
        """
        self.psks: TimedDict[str, Optional[bytes]] = TimedDict(
            time_limit, max_simultaneous_authorizations
        )
        self.ca_certificate = ca_certificate
        self.ca_certificate_key = ca_certificate_key

    def add_psk(self, requestor: str, psk: Optional[bytes]) -> None:
        """
        Instructs this object to wait for a future IssueCertificate request
        from a requestor.

        Parameters:
            requestor: a peer identification string (to tell potential
            requestors apart)
            psk: a pre-shared key, 32 bytes, which the requestor must possess

        If the PSK passed is None, then upon certificate issuance the requestor
        will be told that our side has not yet authenticated the request for
        certificate issuance, and to retry the request later (this is signaled
        via the exception Pending).  If, however, the PSK is valid, then it
        will be used to authenticate the requestor's certificate request.

        Instructions logged with this method are only valid for 60 seconds.

        This method is thread-safe.
        """
        if psk is not None:
            check_psk(psk)
        self.psks[requestor] = psk

    def issue_certificate(
        self,
        requestor: str,
        request: EncryptedCertificateRequest,
    ) -> Tuple[EncryptedClientCertificate, EncryptedRootCertificate]:
        """
        Issues a certificate to a client, if and only if:

        * the peer has a registered PSK (with add_psk)
        * the PSK is not None
        * the request can be decrypted using the peer's PSK

        If the peer's PSK is None, an exception Pending is raised.

        If the peer has no registered PSK, raises UnknownRequestor.

        If the request is well-formed but cannot be decrypted, an exception
        CannotDecrypt is raised.

        If successful, it returns to the caller two items:

        1. a certificate, issued and signed by the CA, encrypted with the PSK
        2. a root of trust certificate, encrypted with the PSK.

        The caller may use the first certificate as its client identity
        certificate, and may use the second certificate to validate the
        identity of the servers it may connect with the first.

        This method is thread-safe.
        """
        with self.psks:
            try:
                psk = self.psks[requestor]
                del self.psks[requestor]
            except KeyError:
                try:
                    # Useful for testing.  Cannot be abused via
                    # production gRPC calls, as no peer ever is
                    # "*" and this value is not under the control
                    # of the peer.
                    psk = self.psks["*"]
                    del self.psks["*"]
                except KeyError:
                    raise UnknownRequestor(requestor)

        if psk is None:
            raise Pending()

        try:
            csr = request.decrypt(psk)
        except (InvalidKey, InvalidSignature, InvalidTag) as e:
            raise CannotDecrypt(e)

        cert = issue_certificate(
            csr,
            self.ca_certificate,
            self.ca_certificate_key,
        )

        enc_cert = EncryptedClientCertificate.encrypt(cert, psk)
        enc_root = EncryptedRootCertificate.encrypt(self.ca_certificate, psk)
        return enc_cert, enc_root


__all__ = [
    x.__name__
    for x in [
        Pending,
        CannotDecrypt,
        UnknownRequestor,
        CA,
    ]
]
