# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_asoulcnki']

package_data = \
{'': ['*'], 'nonebot_plugin_asoulcnki': ['templates/*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-htmlrender>=0.0.4',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-asoulcnki',
    'version': '0.2.1',
    'description': 'ASoulCnki plugin for Nonebot2',
    'long_description': '# nonebot-plugin-asoulcnki\n\nNoneBot 枝网查重插件\n\n利用 [枝网查重](https://asoulcnki.asia/) 查找最相似的小作文，为防止文字太长刷屏，将内容转换为图片形式发出\n\n### 使用方式\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n- 查重/枝网查重 + 要查重的小作文\n\n- 回复需要查重的内容，回复“查重”\n\n- 小作文/随机小作文\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_asoulcnki\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_asoulcnki\n```\n\n\n### 示例\n\n<div align="left">\n  <img src="./examples/1.png" width="500" />\n</div>\n\n\n### 特别感谢\n\n- [ASoulCnki/ASoulCnkiFrontEndV3](https://github.com/ASoulCnki/ASoulCnkiFrontEndV3) 参考了该项目的界面和查重代码\n\n- [cscs181/QQ-GitHub-Bot](https://github.com/cscs181/QQ-GitHub-Bot) 参考了 playwright 的使用以及图片生成的方式\n\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-asoulcnki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
