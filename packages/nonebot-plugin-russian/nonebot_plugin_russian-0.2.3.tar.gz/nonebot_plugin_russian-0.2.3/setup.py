# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_russian']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-russian',
    'version': '0.2.3',
    'description': 'Nonebot2插件 俄罗斯轮盘',
    'long_description': None,
    'author': 'HibiKier',
    'author_email': '775757368@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
