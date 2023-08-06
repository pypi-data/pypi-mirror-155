# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_simplemusic']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-simplemusic',
    'version': '0.1.2',
    'description': '适用于 Nonebot2 的点歌插件',
    'long_description': '# nonebot-plugin-simplemusic\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的点歌插件\n\n支持 qq、网易云、酷我、酷狗、咪咕、b站音频区\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_simplemusic\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_simplemusic\n```\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n```\n点歌/qq点歌/网易点歌/酷我点歌/酷狗点歌/咪咕点歌/b站点歌 + 关键词\n```\n默认为qq点歌\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-simplemusic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
