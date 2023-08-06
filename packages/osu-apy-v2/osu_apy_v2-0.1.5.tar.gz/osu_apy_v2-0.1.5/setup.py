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
    'version': '0.1.5',
    'description': 'small osu api v2 helper',
    'long_description': 'handles refreshing the access_token and stores a mapping of known osu player names and ids in a sqlite database.\\\nread the [osu!api v2 Docs](https://osu.ppy.sh/docs/index.html)\n\n```console\npip install osu-apy-v2\n```\n\n```py\nfrom osu_apy_v2 import OsuApiV2\n\napi = OsuApiV2(application_id, application_secret)\nuser_id = api.get_user_id("whitecat")\nres = api.get(f"/users/{user_id}/scores/best?mode=osu&limit=1")\nprint(res.json())\n```\n',
    'author': 'Eulentier161',
    'author_email': 'eulentier161@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/Eulentier161/osu_apy_v2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
