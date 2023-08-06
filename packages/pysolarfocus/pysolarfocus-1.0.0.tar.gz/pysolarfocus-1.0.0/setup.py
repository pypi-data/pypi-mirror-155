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
    'version': '1.0.0',
    'description': 'Unofficial, local Solarfocus client',
    'long_description': "# pysolarfocus: Python Client for Solarfocus eco<sup>_manager-touch_</sup>\n\n## What's Supported \n\n### Software Version\n\nThis integration has been tested with Solarfocus eco<sup>manager-touch</sup> version `21.040`.\n\n### Solarfocus Components\n\n| Components | Supported |\n|---|---|\n| Heating Circuit 1 (_Heizkreis_)| :white_check_mark: |\n| Buffer 1 (_Puffer_) | :white_check_mark: |\n| Solar (_Solar_)| :x:|\n| Boiler 1 (_Boiler_) | :white_check_mark: |\n| Heatpump (_Wärmepumpe_) | :white_check_mark: |\n| Pelletsboiler (_Kessel_) | :x: | \n\n_Note: The number of supported Heating Circuits, Buffers, and Boilers could be extended in the future_\n",
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
