from typing import Tuple, Optional
import datetime

import socket
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import (
    Certificate,
    CertificateSigningRequest,
    CertificateBuilder,
    random_serial_number,
)
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

NON_CA_USAGES = x509.KeyUsage(
    digital_signature=True,
    content_commitment=True,
    data_encipherment=True,
    key_encipherment=True,
    key_cert_sign=False,
    key_agreement=False,
    crl_sign=False,
    encipher_only=False,
    decipher_only=False,
)
CA_USAGES = x509.KeyUsage(
    digital_signature=True,
    content_commitment=True,
    data_encipherment=True,
    key_encipherment=True,
    key_cert_sign=True,
    key_agreement=True,
    crl_sign=True,
    encipher_only=False,
    decipher_only=False,
)
NON_CA_EXTENDED_KEY_USAGES = x509.ExtendedKeyUsage(
    [
        x509.OID_SERVER_AUTH,
        x509.OID_CLIENT_AUTH,
    ]
)
CA_EXTENDED_KEY_USAGES = x509.ExtendedKeyUsage([x509.OID_EXTENDED_KEY_USAGE])
CA_CONSTRAINTS = x509.BasicConstraints(ca=True, path_length=None)
NON_CA_CONSTRAINTS = x509.BasicConstraints(ca=False, path_length=None)


def create_certificate_and_key(
    cn: Optional[str] = None,
    org: str = "pskca",
    ca: bool = False,
) -> Tuple[Certificate, rsa.RSAPrivateKey]:
    """
    Creates a 4096-bit RSA certificate and associated private key.

    Parameters:
        cn: will be used as the common name in the certificate, if
        present.  If absent / None, the hostname of the system where
        this runs will be used.
        org: will be used as the organization name in the certificate
        if it's specified.  If absent, the organization name will
        simply be "pskca".
        ca: if True, the certificate will be valid as a certificate
        authority allowed to issue and sign other certificates.

    Returns a tuple of (RSA cert, RSA privkey).
    """

    # Create a key pair.
    k = rsa.generate_private_key(65537, 4096)
    p = k.public_key()
    servername = cn if cn is not None else socket.gethostname()

    name = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "XX"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "No city"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
            x509.NameAttribute(NameOID.COMMON_NAME, servername),
        ]
    )
    now = datetime.datetime.utcnow()
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    cert = (
        CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .serial_number(random_serial_number())
        .public_key(p)
        .not_valid_before(now)
        .not_valid_after(expiry)
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(servername)]),
            critical=False,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(p),
            critical=False,
        )
    )

    if ca:
        cert = cert.add_extension(CA_CONSTRAINTS, critical=True)
        cert = cert.add_extension(CA_USAGES, critical=False)
    else:
        cert = cert.add_extension(NON_CA_CONSTRAINTS, critical=False)
        cert = cert.add_extension(NON_CA_USAGES, critical=False)

    return cert.sign(k, hashes.SHA256()), k


def create_certificate_signing_request(
    cn: Optional[str] = None,
) -> Tuple[CertificateSigningRequest, RSAPrivateKey]:
    """
    Generate a certificate signing request.

    Parameters:
        cn: optional client name (used as common name in the certificate
        signing request), will be the hostname of the machine if omitted.

    Returns a tuple of (RSA CSR, RSA privkey).
    """
    servername = cn if cn is not None else socket.gethostname()

    # Create a key pair.
    k = rsa.generate_private_key(65537, 4096)
    # create a CSR (unsigned)
    c = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(
            x509.Name(
                [
                    # Provide various details about who we are.
                    x509.NameAttribute(NameOID.COMMON_NAME, servername),
                ]
            )
        )
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    # Describe what sites we want this certificate for.
                    x509.DNSName(servername),
                ]
            ),
            critical=False,
            # Sign the CSR with our private key.
        )
        .sign(k, hashes.SHA256())
    )

    return c, k


def issue_certificate(
    csr: CertificateSigningRequest,
    root_cert: Certificate,
    root_privkey: RSAPrivateKey,
    validity: datetime.timedelta = datetime.timedelta(days=3650),
    ca: bool = False,
) -> Certificate:
    """
    Using a root CA certificate, issue a certificate based on the supplied
    certificate signing request.

    Parameters:
        csr: the signing request
        root_cert: the root certificate authorized to sign CSRs
        root_privkey: the private key of the root certificate
        validity: ten years by default, another timedelta if you specify it
        ca: if True, the issued certificate is allowed to sign other
        certificates
    """
    now = datetime.datetime.utcnow()
    expiry = datetime.datetime.utcnow() + validity
    SAN = csr.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    if SAN:
        sanvalue = SAN.value
    else:
        sanvalue = None

    cert = CertificateBuilder().subject_name(csr.subject)
    if sanvalue is not None:
        cert = cert.add_extension(
            sanvalue,
            critical=False,
        )
    cert = (
        cert.issuer_name(root_cert.subject)
        .public_key(csr.public_key())
        .serial_number(random_serial_number())
        .not_valid_before(now)
        .not_valid_after(expiry)
    )
    cert = cert.add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(
            root_cert.public_key(),
        ),
        critical=False,
    )

    if ca:
        cert = cert.add_extension(CA_CONSTRAINTS, critical=True)
        cert = cert.add_extension(CA_USAGES, critical=False)
    else:
        cert = cert.add_extension(NON_CA_CONSTRAINTS, critical=False)
        cert = cert.add_extension(NON_CA_USAGES, critical=False)

    return cert.sign(root_privkey, hashes.SHA256())


__all__ = [
    x.__name__
    for x in [
        create_certificate_and_key,
        create_certificate_signing_request,
        issue_certificate,
    ]
]
