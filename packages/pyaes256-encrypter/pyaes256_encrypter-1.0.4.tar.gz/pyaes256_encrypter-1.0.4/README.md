# pyaes256_encrypter
A package to simplify the use of AES-256 encryption with random initialization vector.

## Install
```
pip install pyaes256-encrypter
```

## Usage
~~~python
from pyaes256_encrypter import encode_text, decode_text

# text to be encrypted
text = 'hello world'
# encryption key
key = 'key'


# 'Dx3dCTUSXzzM8wn1L/+NHVbyaDxZFpdqe+SN2NVZgfE='
encoded = encode_text(text,key)
# 'hello world'
decoded = decode_text(encoded,key)
~~~
