from typing import Tuple, List

from cryptography.x509 import (
    Certificate,
    CertificateSigningRequest,
)
from pskca.ca import CannotDecrypt
from pskca.types import (
    EncryptedCertificateRequest,
    EncryptedClientCertificate,
    EncryptedCertificateChain,
)
from cryptography.exceptions import InvalidKey, InvalidSignature, InvalidTag


class Requestor(object):
    """
    The requestor negotiates with the CA (based on a pre-shared key) the
    issuance of a client certificate and the retrieval of the root of trust
    certificate from the CA.
    """

    def __init__(
        self,
        psk: bytes,
    ) -> None:
        """
        Initializes the requestor.

        Parameters:
            psk: a pre-shared key, 32 bytes, which the requestor must possess
            channel: a grpc.Channel, that does not need to be encrypted, to
            the authentication endpoint.
        """
        self.psk = psk

    def encrypt_csr(
        self,
        csr: CertificateSigningRequest,
    ) -> EncryptedCertificateRequest:
        """
        Step 1 in the use of the Requestor class.  This creates the encrypted
        certificate signing request to be sent to the peer.

        Parameters:
            csr: a certificate signing request to be encrypted with the PSK.
        """
        encrypted_csr = EncryptedCertificateRequest.encrypt(csr, self.psk)
        return encrypted_csr

    def decrypt_reply(
        self,
        encrypted_issued_cert: EncryptedClientCertificate,
        encrypted_root_cert: EncryptedCertificateChain,
    ) -> Tuple[Certificate, List[Certificate]]:
        """
        Step 2 in the use of the Requestor class.  After obtaining a response
        from the server (which contains two fields, the issued certificate
        and the root of trust certificate) pass these fields to this function
        to receive the two certificates (issued, and root of trust)

        Parameters:
           encrypted_issued_cert: the encrypted client certificate part of the
           IssueCertificateReply from the CA.  If you have the bytes-serialized
           object, you can create the right type thus:
           ```
           enc_cert = pskca.EncryptedClientCertificate(blob)
           ```
           encrypted_root_cert: the encrypted root of trust certificate part of
           the IssueCertificateReply from the CA.  If you have the bytes-
           serialized object, you can creaty the right type thus
           ```
           enc_cert = pskca.EncryptedCertificateChain(blob)
           ```

        Returns a tuple with:
        * the issued certificate for the client to identify to the server
        * the root of trust certificate for the client to identify the server
        """
        try:
            return (
                encrypted_issued_cert.decrypt(self.psk),
                encrypted_root_cert.decrypt(self.psk),
            )
        except (InvalidKey, InvalidSignature, InvalidTag) as e:
            raise CannotDecrypt(e)


__all__ = ["Requestor"]
