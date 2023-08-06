# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autotst']

package_data = \
{'': ['*']}

install_requires = \
['autogluon>=0.4.2,<0.5.0',
 'importlib-metadata>=1.4',
 'nptyping>=1.4.4,<2.0.0',
 'numpy>=1.21,<2.0',
 'pandas>=1.3,<2.0',
 'pytest>=7.1.2,<8.0.0',
 'torchvision==0.11.3']

setup_kwargs = {
    'name': 'autotst',
    'version': '1.0',
    'description': 'two-samples testing and distribution shift detection',
    'long_description': None,
    'author': 'Jonas M. Kübler',
    'author_email': 'jonas.m.kuebler@tuebingen.mpg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
