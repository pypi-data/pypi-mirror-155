# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orcha',
 'orcha.bin',
 'orcha.exceptions',
 'orcha.interfaces',
 'orcha.lib',
 'orcha.plugins',
 'orcha.utils']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0',
 'python-daemon>=2.3.0,<3.0.0',
 'systemd-python>=234,<235']

extras_require = \
{'docs': ['Sphinx>=4.3.2,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinx-autodoc-annotation>=1.0-1,<2.0']}

setup_kwargs = {
    'name': 'orcha',
    'version': '0.1.12',
    'description': 'System handler and orchestrator of multiple environments',
    'long_description': None,
    'author': 'Javier Alonso',
    'author_email': 'jalonso@teldat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
