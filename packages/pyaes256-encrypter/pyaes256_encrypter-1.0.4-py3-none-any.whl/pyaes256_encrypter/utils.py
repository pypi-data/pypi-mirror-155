def generate_cipher(key:str,iv=None):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import hashlib
    import os

    backend = default_backend()
    key = hashlib.sha256(key.encode()).digest()

    if iv == None:
        iv = os.urandom(16)

    aes = algorithms.AES(key)
    ctr = modes.CTR(iv)

    return {
        'cipher': Cipher(aes, ctr, backend=backend),
        'iv': iv
    } 


def formate_text(text:str):
    return bytearray(text+' '*(16-(len(bytearray(text,encoding="ascii"))%16)),encoding="utf8")