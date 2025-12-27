import os
import hmac
import hashlib

P = 23
G = 5


def dh_generate_private():
    return int.from_bytes(os.urandom(2), "big")


def dh_generate_public(priv):
    return pow(G, priv, P)


def dh_compute_shared(pub, priv):
    return pow(pub, priv, P)


def derive_keys(shared_secret: int):
    digest = hashlib.sha256(shared_secret.to_bytes(2, "big")).digest()
    otp = digest[:16]
    mac = digest[16:]
    return otp, mac


def otp_encrypt(key: bytes, plaintext: bytes, counter: int = 0) -> bytes:
    ciphertext = bytearray()
    key_len = len(key)
    for i, b in enumerate(plaintext):
        k = key[(i + counter) % key_len]
        ciphertext.append(b ^ k)
    return bytes(ciphertext)


def otp_decrypt(key: bytes, ciphertext: bytes, counter: int = 0) -> bytes:
    return otp_encrypt(key, ciphertext, counter)


def encrypt_then_mac(
    otp_key: bytes, mac_key: bytes, plaintext: bytes, counter: int = 0
) -> bytes:
    ciphertext = otp_encrypt(otp_key, plaintext, counter)
    mac = hmac.new(mac_key, ciphertext, hashlib.sha256).digest()
    return ciphertext + mac


def verify_then_decrypt(
    otp_key: bytes, mac_key: bytes, data: bytes, counter: int = 0
) -> bytes:
    if len(data) < 32:
        raise ValueError("Odebrano zbyt krótką wiadomość")
    ciphertext = data[:-32]
    mac_received = data[-32:]
    mac_calculated = hmac.new(mac_key, ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(mac_received, mac_calculated):
        raise ValueError("MAC verification failed")
    return otp_decrypt(otp_key, ciphertext, counter)
