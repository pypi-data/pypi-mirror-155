import secrets
from typing import cast, TypeVar, Type, List

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.x509 import (
    load_pem_x509_certificate,
    Certificate,
    CertificateSigningRequest,
    load_pem_x509_csr,
)


NONCE_LENGTH = 12


def check_psk(psk: bytes) -> None:
    if not isinstance(psk, bytes):
        raise ValueError("invalid PSK (not bytes)")
    if len(psk) != 32:
        raise ValueError("invalid PSK length (%d != 32)" % len(psk))


class EncryptedPayload(bytes):
    def __init__(self, bytearray: bytes):
        if len(bytearray) > 16384:
            raise ValueError("%ss cannot be over 16KiB" % self.__class__)
        super().__init__()

    @classmethod
    def encrypt(klass, payload: bytes, psk: bytes) -> "EncryptedPayload":
        check_psk(psk)
        chacha = ChaCha20Poly1305(psk)
        plaintext_nonce = secrets.token_bytes(12)
        encrypted_payload = chacha.encrypt(
            plaintext_nonce,
            payload,
            plaintext_nonce,
        )
        return klass(
            b"".join(
                [
                    plaintext_nonce,
                    encrypted_payload,
                ]
            ),
        )

    def decrypt(self, psk: bytes) -> bytes:
        check_psk(psk)
        chacha = ChaCha20Poly1305(psk)
        plaintext_nonce = self[:NONCE_LENGTH]
        encrypted_csr = self[NONCE_LENGTH:]
        decrypted = chacha.decrypt(
            plaintext_nonce,
            encrypted_csr,
            plaintext_nonce,
        )
        return decrypted

    def to_bytes(self) -> bytes:
        """
        Returns self's representation as bytes.
        """
        return cast(bytes, self)


class EncryptedCertificateRequest(object):
    """
    Represents an encrypted certificate request.
    """

    def __init__(self, bytearray: bytes):
        """
        Initializes an EncryptedCertificateRequest based on a byte array.
        """
        self.payload = EncryptedPayload(bytearray)

    @classmethod
    def encrypt(
        klass, csr: CertificateSigningRequest, psk: bytes
    ) -> "EncryptedCertificateRequest":
        """
        Takes CSR and encrypts it using the PSK.

        Returns a bytes package of the CSR, which can be sent over the wire.
        """
        csr_bytes = csr.public_bytes(serialization.Encoding.PEM)
        return klass(
            EncryptedPayload.encrypt(
                csr_bytes,
                psk,
            )
        )

    def decrypt(self, psk: bytes) -> CertificateSigningRequest:
        """
        Decrypts the encrypted certificate signing request and returns it.
        """
        decrypted = self.payload.decrypt(psk)
        return load_pem_x509_csr(decrypted)

    def to_bytes(self) -> bytes:
        """
        Returns an EncryptedCertificateRequest package which can then be sent
        over the wire by calling its `.to_bytes()` method.
        """
        return self.payload.to_bytes()


class EncryptedCertificate(object):
    def __init__(self, bytearray: bytes):
        """
        Initializes an EncryptedCertificate based on a byte array.
        """
        self.payload = EncryptedPayload(bytearray)

    @classmethod
    def encrypt(
        klass: Type["EncCertType"],
        certificate: Certificate,
        psk: bytes,
    ) -> "EncCertType":
        """
        Takes the certificate (which may be an issued certificate or a CA
        certificate), and encrypts it using the PSK.

        Returns a new EncryptedCertificate object, which can then be sent
        over the wire by calling its `.to_bytes()` method.
        """
        cert_bytes = certificate.public_bytes(serialization.Encoding.PEM)
        return klass(
            EncryptedPayload.encrypt(
                cert_bytes,
                psk,
            )
        )

    def decrypt(self, psk: bytes) -> Certificate:
        """
        Decrypts the encrypted certificate signing request and returns it.
        """
        decrypted = self.payload.decrypt(psk)
        return load_pem_x509_certificate(decrypted)

    def to_bytes(self) -> bytes:
        """
        Returns self's representation as bytes.  Use this to serialize the
        encrypted package to an array of bytes, for sending over the wire.
        """
        return self.payload.to_bytes()


EncCertType = TypeVar("EncCertType", bound=EncryptedCertificate)


class EncryptedClientCertificate(EncryptedCertificate):
    """
    Represents a client certificate issued by the CA.

    Clients will use this as their identity certificate to do mutual TLS
    authentication against servers whose certificates are secured by the CA.
    """


class EncryptedCertificateChain(object):
    """
    Represents a list of certificates that are the root of trust.  It must
    be a list of certificates ordered by height -- signers go before signees.
    For more information on ordering, see
    https://cheapsslsecurity.com/p/what-is-ssl-certificate-chain/

    Clients will use this chain as their root of trust to do mutual TLS
    authentication against servers whose certificates are secured by the CA.
    """

    def __init__(self, bytearray: bytes) -> None:
        """
        Initializes an EncryptedCertificateChain based on a byte array.
        """
        self.payload = EncryptedPayload(bytearray)

    @classmethod
    def encrypt(
        klass: Type["EncChainType"],
        certificate_chain: List[Certificate],
        psk: bytes,
    ) -> "EncChainType":
        """
        Takes the certificate chain and encrypts it using the PSK.

        Returns an EncryptedCertificateChain package which can safely be sent
        over the wire by calling its `.to_bytes()` method.
        """
        cert_bytes: List[bytes] = []
        for cert in certificate_chain:
            cert_bytes.append(cert.public_bytes(serialization.Encoding.PEM))
        cert_bytes_string = b"\n".join(cert_bytes)
        return klass(
            EncryptedPayload.encrypt(
                cert_bytes_string,
                psk,
            )
        )

    def decrypt(self, psk: bytes) -> List[Certificate]:
        """
        Decrypts the encrypted certificate signing request and returns it.
        """
        decrypted = self.payload.decrypt(psk)
        start_line = b"-----BEGIN CERTIFICATE-----"
        cert_slots = decrypted.split(start_line)
        certificates: List[Certificate] = []
        for single_pem_cert in cert_slots[1:]:
            loaded = load_pem_x509_certificate(start_line + single_pem_cert)
            certificates.append(loaded)
        return certificates

    def to_bytes(self) -> bytes:
        """
        Returns a bytes-serialized array package which can safely be sent
        over the wire.
        """
        return self.payload.to_bytes()


EncChainType = TypeVar("EncChainType", bound=EncryptedCertificateChain)


__all__ = [
    x.__name__
    for x in [
        EncryptedCertificateRequest,
        EncryptedClientCertificate,
        EncryptedCertificateChain,
        check_psk,
    ]
]
