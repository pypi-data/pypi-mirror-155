# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_ddcheck']

package_data = \
{'': ['*'], 'nonebot_plugin_ddcheck': ['template/*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0',
 'nonebot-plugin-htmlrender>=0.0.4',
 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ddcheck',
    'version': '0.1.5',
    'description': 'Nonebot2 成分姬插件',
    'long_description': '# nonebot-plugin-ddcheck\n\nNoneBot2 成分姬插件\n\n查询B站关注列表的VTuber成分，并以图片形式发出\n\nVTB列表数据来源：[vtbs.moe](https://vtbs.moe/)\n\n\n### 使用方式\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n```\n查成分 + B站用户名/UID\n```\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_ddcheck\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_ddcheck\n```\n\n若要显示主播牌子，需要在 `.env.xxx` 文件中添加任意的B站用户cookie：\n\n```\nbilibili_cookie=xxx\n```\n\n\n### 示例\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/03/20/Nk3jZJgxforHDsu.png" width="400" />\n</div>\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MeetWq/nonebot-plugin-ddcheck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
