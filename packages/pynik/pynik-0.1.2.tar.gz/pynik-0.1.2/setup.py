# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynik', 'pynik.libs.src']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'pynik',
    'version': '0.1.2',
    'description': '',
    'long_description': '=====\npynik\n=====\n\nThis is purely a project trying out packaging of python\ncode to Pypi.\n\nTrying out Styling guide\n------------------------\n\nThis also outlines some of the ways of formatting text\nwith rst, which is unfamiliar.\n',
    'author': 'Nik Sheridan',
    'author_email': 'nik.sheridan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
