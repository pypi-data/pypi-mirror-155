# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_handle']

package_data = \
{'': ['*'], 'nonebot_plugin_handle': ['resources/data/*', 'resources/fonts/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.4,<3.0.0',
 'pypinyin>=0.40.0']

setup_kwargs = {
    'name': 'nonebot-plugin-handle',
    'version': '0.1.4',
    'description': 'Nonebot2 汉字Wordle 插件',
    'long_description': '# nonebot-plugin-handle\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的 汉字Wordle 猜成语插件\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_handle\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_handle\n```\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n```\n@机器人 + 猜成语\n```\n\n你有十次的机会猜一个四字词语；\n\n每次猜测后，汉字与拼音的颜色将会标识其与正确答案的区别；\n\n青色 表示其出现在答案中且在正确的位置；\n\n橙色 表示其出现在答案中但不在正确的位置；\n\n当四个格子都为青色时，你便赢得了游戏！\n\n可发送“结束”结束游戏；可发送“提示”查看提示。\n\n\n或使用 `handle` 指令：\n\n```\nhandle [--hint] [--stop] [idiom]\n```\n\n\n### 示例\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/03/29/MVrKPdR2i9sQSfm.png" width="400" />\n</div>\n\n\n### 特别感谢\n\n- [antfu/handle](https://github.com/antfu/handle) A Chinese Hanzi variation of Wordle - 汉字 Wordle\n- [AllanChain/chinese-wordle](https://github.com/AllanChain/chinese-wordle) Chinese idiom wordle game | 仿 wordle 的拼成语游戏\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-handle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
