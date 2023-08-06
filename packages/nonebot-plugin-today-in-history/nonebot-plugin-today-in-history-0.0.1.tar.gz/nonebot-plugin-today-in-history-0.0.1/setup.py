# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_today_in_history']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nonebot-plugin-today-in-history',
    'version': '0.0.1',
    'description': 'Send Today In History to friends or group chat',
    'long_description': None,
    'author': 'AquamarineCyan',
    'author_email': '1057424730@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
