# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iflags']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iflags',
    'version': '1.0.3',
    'description': 'A Generic flags parser based on argparse',
    'long_description': None,
    'author': 'maybaby',
    'author_email': 'ybyang7@iflytek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
