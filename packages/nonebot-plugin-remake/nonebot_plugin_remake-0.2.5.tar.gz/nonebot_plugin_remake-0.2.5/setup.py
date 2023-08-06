# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_remake']

package_data = \
{'': ['*'], 'nonebot_plugin_remake': ['resources/*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0', 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-remake',
    'version': '0.2.5',
    'description': '适用于 Nonebot2 的人生重开模拟器插件',
    'long_description': '# nonebot-plugin-remake\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的人生重开模拟器\n\n这垃圾人生一秒也不想待了？立即重开！\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_remake\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_remake\n```\n\n\n### 使用\n\n#### 触发方式：\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n```\n@机器人 remake/liferestart/人生重开/人生重来\n```\n\n\n#### 示例：\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/01/15/rahwIWFfuvLGPgm.jpg" width="400" />\n</div>\n\n\n### 特别感谢\n\n- [cc004/lifeRestart-py](https://github.com/cc004/lifeRestart-py) lifeRestart game in python\n\n- [DaiShengSheng/lifeRestart_bot](https://github.com/DaiShengSheng/lifeRestart_bot) 适用于HoshinoBot下的人生重来模拟器插件\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-remake',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
