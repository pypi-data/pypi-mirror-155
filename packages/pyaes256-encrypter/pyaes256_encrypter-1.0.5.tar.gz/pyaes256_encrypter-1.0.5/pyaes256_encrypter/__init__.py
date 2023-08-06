__version__ = '1.0.5'

from pyaes256_encrypter.utils import generate_cipher,formate_text

def encode_text(text:str,key:str):
    import base64

    formated_text = formate_text(text)

    cipher_data = generate_cipher(key)
    iv = cipher_data['iv']
    cipher = cipher_data['cipher']

    encryptor = cipher.encryptor()
    aes256encoded = iv + encryptor.update(formated_text) + encryptor.finalize()
    
    return base64.b64encode(aes256encoded).decode()


def decode_text(text:str,key:str):
    import base64
    
    aes256_hash = base64.b64decode(text.encode())

    iv = aes256_hash[slice(16)]
    encoded_text = aes256_hash.split(iv)[1]

    cipher_data = generate_cipher(key,iv)
    cipher = cipher_data['cipher']

    decryptor = cipher.decryptor()

    decoded_text = decryptor.update(encoded_text) + decryptor.finalize()
    return decoded_text.decode().strip()