# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['h_devops']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.9.1,<6.0.0', 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['h-devops = h_devops.main:app']}

setup_kwargs = {
    'name': 'h-devops',
    'version': '0.1.0',
    'description': '',
    'long_description': '# h_devops v1.0.0\n\n# How to install\nPlease run this command on your terminal window\n```shell\n$ pip install h_devops\n```',
    'author': 'Vo Viet Hoang',
    'author_email': 'levuthanhtung11@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
