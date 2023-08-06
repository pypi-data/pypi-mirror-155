# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaes256_encrypter']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.0']

setup_kwargs = {
    'name': 'pyaes256-encrypter',
    'version': '1.0.6',
    'description': 'A package to simplify the use of AES-256 encryption with random initialization vector.',
    'long_description': "# pyaes256_encrypter\nA package to simplify the use of AES-256 encryption with random initialization vector.\n\n## Install\n```\npip install pyaes256-encrypter\n```\n\n## Usage\n~~~python\nfrom pyaes256_encrypter import encode_text, decode_text\n\n# text to be encrypted\ntext = 'hello world'\n# encryption key\nkey = 'key'\n\n\n# RANDOM ENCODED e.g. 'Dx3dCTUSXzzM8wn1L/+NHVbyaDxZFpdqe+SN2NVZgfE='\nencoded = encode_text(text, key)\n# 'hello world'\ndecoded = decode_text(encoded, key)\n~~~\n",
    'author': 'Maicon Renildo',
    'author_email': 'maicon.renildo1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
