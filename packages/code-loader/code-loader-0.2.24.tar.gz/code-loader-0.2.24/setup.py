# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_loader',
 'code_loader.contract',
 'code_loader.leap_binder',
 'code_loader.visualizers']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'tensorflow>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'code-loader',
    'version': '0.2.24',
    'description': '',
    'long_description': '# tensorleap code loader\nUsed to load user code to tensorleap \n',
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tensorleap/code-loader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
