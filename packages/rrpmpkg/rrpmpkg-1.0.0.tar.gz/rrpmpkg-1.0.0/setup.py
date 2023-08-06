# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrpmpkg']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0', 'rich>=12.4.4,<13.0.0', 'typer>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'rrpmpkg',
    'version': '1.0.0',
    'description': "RRPM's Package Manager",
    'long_description': None,
    'author': 'pybash1',
    'author_email': '67195650+pybash1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
