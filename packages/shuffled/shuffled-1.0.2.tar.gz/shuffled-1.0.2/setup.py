# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shuffled']

package_data = \
{'': ['*']}

install_requires = \
['cryptography']

setup_kwargs = {
    'name': 'shuffled',
    'version': '1.0.2',
    'description': 'Iterate randomly over integer ranges',
    'long_description': "# Shuffled: Random iterators for large integer ranges\n\nShuffled is a library for iterating randomly and without repetition over integer ranges.\nIt doesn't store all the integers in memory so that you can work with ranges of up to\n2<sup>128</sup> elements, even with your standard RAM available.\n\n```python\n>>> shuffled_range = Shuffled(10)\n>>> list(shuffled_range)\n[4, 1, 2, 9, 8, 5, 3, 0, 6, 7]\n>>> same_shuffled_range = Shuffled(10, seed=shuffled_range.seed)\n>>> list(same_shuffled_range)\n[4, 1, 2, 9, 8, 5, 3, 0, 6, 7]\n```\n\n```python\n>>> network = ipaddress.IPv4Network('10.0.0.0/8')\n>>> shuffled_range = Shuffled(network.num_addresses)\n>>> for index in shuffled_range:\n...     print(network[index])\n...\n10.24.41.126\n10.67.199.15\n10.240.82.199\n10.79.219.74\n10.166.105.25\n10.19.5.91\n[...]\n```\n",
    'author': 'Bertrand Bonnefoy-Claudet',
    'author_email': 'bertrand@bertrandbc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bbc2/shuffled',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
