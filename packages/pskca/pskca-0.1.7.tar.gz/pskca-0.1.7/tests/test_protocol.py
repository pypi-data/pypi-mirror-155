# type: ignore

import os
import pskca
import pytest


__cached_ca = None
__cached_csr = None


def _cache_ca():
    global __cached_ca
    if __cached_ca is None:
        __cached_ca = pskca.create_certificate_and_key(ca=True)
    return __cached_ca


def _cache_csr():
    global __cached_csr
    if __cached_csr is None:
        __cached_csr = pskca.create_certificate_signing_request()
    return __cached_csr


def init():
    client_id = "xxx"
    psk = os.urandom(32)
    ca_cert, ca_key = _cache_ca()
    client_csr, client_key = _cache_csr()
    return client_id, psk, ca_cert, ca_key, client_csr, client_key


def test_authorized():
    client_id, psk, ca_cert, ca_key, client_csr, client_key = init()

    C = pskca.CA(ca_cert, ca_key, [ca_cert])
    C.add_psk(client_id, psk)
    R = pskca.Requestor(psk)
    payload = R.encrypt_csr(client_csr)
    _, __, enc_client_cert, enc_server_cert = C.issue_certificate(
        client_id,
        payload,
    )
    client_cert, server_cert = R.decrypt_reply(
        enc_client_cert,
        enc_server_cert,
    )


def test_pending():
    client_id, psk, ca_cert, ca_key, client_csr, client_key = init()

    C = pskca.CA(ca_cert, ca_key, [ca_cert])
    C.add_psk(client_id, None)
    R = pskca.Requestor(psk)
    enc = R.encrypt_csr(client_csr)
    with pytest.raises(pskca.Pending):
        _, __, enc_client_cert, enc_server_cert = C.issue_certificate(
            client_id,
            enc,
        )


def test_wrong_key():
    client_id, psk, ca_cert, ca_key, client_csr, client_key = init()
    wrong_psk = os.urandom(32)

    C = pskca.CA(ca_cert, ca_key, [ca_cert])
    C.add_psk(client_id, psk)
    R = pskca.Requestor(wrong_psk)
    enc = R.encrypt_csr(client_csr)
    with pytest.raises(pskca.CannotDecrypt):
        _, __, enc_client_cert, enc_server_cert = C.issue_certificate(
            client_id,
            enc,
        )


def test_unknown_client():
    client_id, psk, ca_cert, ca_key, client_csr, client_key = init()

    C = pskca.CA(ca_cert, ca_key, [ca_cert])
    R = pskca.Requestor(psk)
    enc = R.encrypt_csr(client_csr)
    with pytest.raises(pskca.UnknownRequestor):
        _, __, enc_client_cert, enc_server_cert = C.issue_certificate(
            client_id,
            enc,
        )
