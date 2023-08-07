# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_boardgame']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-datastore>=0.3.0,<0.4.0',
 'nonebot-plugin-htmlrender>=0.0.4',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-boardgame',
    'version': '0.1.6',
    'description': '适用于 Nonebot2 的棋类游戏插件',
    'long_description': '## nonebot-plugin-boardgame\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的棋类游戏插件。\n\n抄自隔壁 koishi（：[koishi-plugin-chess](https://github.com/koishijs/koishi-plugin-chess)\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_boardgame\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_boardgame\n```\n\n\n### 使用\n\n目前支持的规则有：\n\n- 五子棋\n- 围棋（禁全同，暂时不支持点目）\n- 黑白棋\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n\n@机器人 发送 “围棋” 或 “五子棋” 或 “黑白棋” 开始一个对应的棋局，一个群组内同时只能有一个棋局。\n\n发送“落子 字母+数字”下棋，如“落子 A1”；\n\n游戏发起者默认为先手，可使用 `--white` 选项选择后手；\n\n发送“结束下棋”结束当前棋局；\n\n发送“查看棋局”显示当前棋局；\n\n发送“悔棋”可以进行悔棋；\n\n发送“跳过回合”可跳过当前回合（仅黑白棋支持）；\n\n手动结束游戏或超时结束游戏时，可发送“重载xx棋局”继续下棋，如 `重载围棋棋局`；\n\n\n或者使用 `boardgame` 指令：\n\n可用选项：\n - `-r RULE`, `--rule RULE`: 规则名\n - `-e`, `--stop`, `--end`: 停止下棋\n - `-v`, `--show`, `--view`: 显示棋盘\n - `--repent`: 悔棋\n - `--skip`: 跳过回合\n - `--reload`: 重新加载已停止的游戏\n - `--white`: 执白，即后手\n - `POSITION`: 落子位置\n\n\n### 示例\n\n<div align="left">\n    <img src="https://s2.loli.net/2022/06/17/TbaCXSL1u4sd9rV.png" width="400" />\n</div>\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-boardgame',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
