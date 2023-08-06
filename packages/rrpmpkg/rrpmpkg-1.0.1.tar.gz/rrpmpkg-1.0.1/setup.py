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
    'version': '1.0.1',
    'description': "RRPM's Package Manager",
    'long_description': "\n![Logo](https://raw.githubusercontent.com/pybash1/rrpm/master/extra/banner.png)\n\n\n# RRPMPkg\n\nRRPMPkg is the official package manager for [RRPM](https://github.com/rrpm-org/rrpm). It enables you to easily install, uninstall and update all your RRPM extensions.\n## Badges\n\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n\n## Installation\n\nYou can install rrpmpkg from PyPI. If you have RRPM Installed, you most likely also have RRPMPkg installed.\n\n```bash\n$ pip install rrpmpkg\n```\n    \n## Documentation\n\nThe Documentation for RRPMPkg can be found [here](https://pybash.gibook.io/rrpmpkg)\n\n\n## Usage/Examples\n\n```bash\n$ rrpmpkg install rrpm-org/demo-extension # Install extension\n...\n$ rrpmpkg uninstall someotherextension # Uninstall extension\n...\n$ rrpmpkg update # Update all extensions\n...\n$ rrpmpkg update --package demo-extensions # Update specific extension\n```\n\n\n## Authors\n\n- [@pybash1](https://www.github.com/pybash1)\n\n\n## Contributing\n\nContributions are always welcome!\n\nSee [CONTRIBUTING.md](https://github.com/rrpm-org/rrpm/blob/master/CONTRIBUTING.md) for ways to get started.\n\nPlease adhere to this project's [CODE_OF_CONDUCT.md](https://github.com/rrpm-org/rrpm/blob/master/CODE_OF_CONDUCT.md).\n## Feedback\n\nIf you have any feedback, please reach out to me at [@py_bash1](https://twitter.com/py_bash1)\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n",
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
