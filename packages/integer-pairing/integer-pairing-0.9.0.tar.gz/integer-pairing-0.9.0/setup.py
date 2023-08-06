# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['integer_pairing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'integer-pairing',
    'version': '0.9.0',
    'description': '',
    'long_description': '# integer-pairing\n\nThis library enables encodings of integer tuples as one integer. It implements two types of encodings - Cantor and Szudzik.\nThere is a [great article](https://www.vertexfragment.com/ramblings/cantor-szudzik-pairing-functions/) on those two types.\n\n## Usage\nThe base example is\n```python\nfrom integer_pairing import cantor, szudzik\n\ncantor.pair(11, 13) # 313\ncantor.unpair(313) # (11, 13)\n\nszudzik.pair(11, 13) # 180\nszudzik.unpair(180) # (11, 13)\n```\nYou can pair tuples of any size, but have to specify the size when unpairing\n```python\ncantor.pair(11, 13, 17, 19, 23) # 1115111727200556569\ncantor.unpair(1115111727200556569, dim=5) # (11, 13, 17, 19, 23)\n```\nIt is also possible to include negative numbers, but you need to imply that when decoding\n```python \ncantor.pair(11, 13, -1) # 726618\ncantor.unpair(726618, dim=3, neg=True) # (11, 13, -1)\n```\nNaive implementations of the above algorithms, fail to account for very large\nintegers, as they use numeric calculation of the square root. Python allows for \nintegers of any size to be stored, but converts them to float (64 bits) when doing numeric operations, \nso this approximation ruins the unpairing. Luckily this can be (efficiently) solved and is implemented here.\n```python\ncantor.pair(655482261805334959278882253227, 730728447469919519177553911051)\n# 960790065254702046274404114853633027146937669672812473623832\ncantor.unpair(960790065254702046274404114853633027146937669672812473623832)\n# (655482261805334959278882253227, 730728447469919519177553911051)\n```\nYou can also pair things in a way that encodes the tuple\'s dimension and its signs. \nThis is called bundleing and is done by encoding each number in a tuple in binary, \nthen prepending those encodings by the number 2 or 22, depending on its sign.\nFor space-efficiency, the string is then interpreted in a trinary base system.\n```python\nfrom integer_pairing import bundle\n\nbundle.pair(*range(-8,8))\n# 1061264631713144962268472871675\nbundle.unpair(1061264631713144962268472871675)\n# (-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7)\n```\nThe downside here is that `bundle.pair` is not surjective, so not every number can be unpaired. \nCalling unpair on those will produce an exception\n```python\nbundle.unpair(0)\n              \nTraceback (most recent call last):\n  File "<pyshell#37>", line 1, in <module>\n    bundle.unpair(0)\n  File "C:\\Users\\kuco\\integer-pairing\\integer_pairing\\_interface.py", line 66, in unpair\n    return self._unbundle(n)\n  File "C:\\Users\\kuco\\integer-pairing\\integer_pairing\\_bundle.py", line 41, in _unbundle\n    di = 1 if s[i+1] != \'2\' else 2\nIndexError: string index out of range\n```\n\n## Complexity\nThe pairing of n integers will result in an integer of the size of about their product.\n\n## Example usage from Cryptography\nWhen encrypting messages deterministically, an attacker can always reproduce the encryption \nof any chosen messages. If those possibilities are few (like `0` / `1`), those kinds \nof algorithms are pretty useless. This is solved by appending a random number, called salt, \nto the message. It can be useful to implement this appending via pairing.\n```python\nfrom random import getrandbites\n\nsalt = getrandbites(200)\nmessage = 0\nencoded = szudzik.pair(message, salt)\n```\n',
    'author': 'Nejc Ševerkar',
    'author_email': 'nseverkar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kuco23/integer-pairing/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
