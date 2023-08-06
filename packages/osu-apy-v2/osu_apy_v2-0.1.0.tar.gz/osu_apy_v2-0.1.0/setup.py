# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osu_apy_v2']

package_data = \
{'': ['*']}

install_requires = \
['pyaml>=21.10.1,<22.0.0', 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'osu-apy-v2',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Eulentier161',
    'author_email': 'eulentier161@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
