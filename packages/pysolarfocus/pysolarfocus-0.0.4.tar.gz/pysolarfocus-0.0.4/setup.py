# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysolarfocus']

package_data = \
{'': ['*']}

install_requires = \
['pymodbus>=2.5.3,<3.0.0']

setup_kwargs = {
    'name': 'pysolarfocus',
    'version': '0.0.4',
    'description': 'Unofficial, local Solarfocus client',
    'long_description': '# pysolarfocus',
    'author': 'Jeroen Laverman',
    'author_email': 'jjlaverman@web.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lavermanjj/pysolarfocus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
