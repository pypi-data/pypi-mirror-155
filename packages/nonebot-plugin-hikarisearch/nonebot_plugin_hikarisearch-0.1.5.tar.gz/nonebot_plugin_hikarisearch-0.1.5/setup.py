# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_hikarisearch']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-hikarisearch',
    'version': '0.1.5',
    'description': '基于 HikariSearch 的又一个 Nonebot2 搜图插件',
    'long_description': '# nonebot-plugin-hikarisearch\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的搜图插件\n\n使用 [HikariSearch](https://github.com/mixmoe/HikariSearch) 搜索\n\n支持 SauceNAO、IqDB、ascii2d、E-Hentai、TraceMoe\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_hikarisearch\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_hikarisearch\n```\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n```\n搜图/saucenao搜图/iqdb搜图/ascii2d搜图/ehentai搜图/tracemoe搜图 + 图片\n```\n默认为 saucenao搜图\n\n或回复包含图片的消息，回复搜图\n\n或 搜图上一张，搜索上一次出现的图\n\n### 配置\n\n可在 `.env.xxx` 文件中添加如下配置：\n\n```\nhikarisearch_api=xxx  # HikariSearch 站点，默认为 "https://hikari.obfs.dev"\nhikarisearch_max_results=xxx  # 最多返回的结果数量，默认为 3\n```\n\n在群聊中，当搜索结果数量>1时，结果以合并转发的形式发出\n\n私聊时，搜索结果会逐个发出\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-hikarisearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
