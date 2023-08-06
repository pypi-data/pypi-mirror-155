# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_logo']

package_data = \
{'': ['*'],
 'nonebot_plugin_logo': ['templates/*',
                         'templates/fonts/*',
                         'templates/images/*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'imageio>=2.12.0,<3.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-htmlrender>=0.0.4.1',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-logo',
    'version': '0.2.2',
    'description': 'Nonebot2插件，用于制作 PornHub 等风格 logo',
    'long_description': '# nonebot-plugin-logo\n\n[Nonebot2](https://github.com/nonebot/nonebot2) 插件，用于 PornHub 等风格logo制作\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_logo\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_logo\n```\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n目前支持的风格：\n\n - PornHub\n\n指令：`ph /phlogo {left_text} {right_text}`\n\n示例：`ph Porn Hub`\n\n<div align="left">\n  <img src="./examples/1.png" />\n</div>\n\n - YouTube\n\n指令：`yt /ytlogo {left_text} {right_text}`\n\n示例：`yt You Tube`\n\n<div align="left">\n  <img src="./examples/2.png" />\n</div>\n\n - 5000兆円欲しい!\n\n指令：`5000兆 {left_text} {right_text}`\n\n示例：`5000兆 我去 初音未来`\n\n<div align="left">\n  <img src="./examples/3.png" />\n</div>\n\n - 抖音\n\n指令：`douyin/dylogo {text}`\n\n示例：`douyin douyin`\n\n<div align="left">\n  <img src="./examples/4.gif" />\n</div>\n\n - 谷歌\n\n指令：`google/gglogo {text}`\n\n示例：`google Google`\n\n<div align="left">\n  <img src="./examples/5.png" />\n</div>\n\n\n### 特别感谢\n\n- [yurafuca/5000choyen](https://github.com/yurafuca/5000choyen) 5000choyen generator\n\n- [Ice-Hazymoon/MikuTools](https://github.com/Ice-Hazymoon/MikuTools) 一个轻量的工具集合\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-logo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
