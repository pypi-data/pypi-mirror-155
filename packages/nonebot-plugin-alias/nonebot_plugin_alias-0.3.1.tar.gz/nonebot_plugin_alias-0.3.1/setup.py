# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_alias']

package_data = \
{'': ['*']}

install_requires = \
['expandvars>=0.7.0,<0.8.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-alias',
    'version': '0.3.1',
    'description': 'A simple plugin for adding aliases for Nonebot command',
    'long_description': '# nonebot-plugin-alias\n\n为 [nonebot2](https://github.com/nonebot/nonebot2) 的指令创建别名\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n- `alias [别名]=[指令名称]` 添加别名\n- `alias [别名]` 查看别名\n- `alias -p` 查看所有别名\n- `unalias [别名]` 删除别名\n- `unalias -a` 删除所有别名\n\n默认只在当前群聊/私聊中生效，使用 `-g` 参数添加全局别名；增删全局别名需要超级用户权限\n\n- `alias -g [别名]=[指令名称]` 添加全局别名\n- `unalias -g [别名]` 删除全局别名\n\n### 示例\n\n<div align="left">\n  <img src="./examples/1.png" width="300" />\n  <img src="./examples/2.png" width="300" />\n</div>\n\n### 传入参数\n\n可以用 bash shell 的风格在别名中使用参数，如：`alias test="echo $1"`\n\n`$1` 表示第一个参数，以此类推；`$a` 表示所有参数\n\n**当创建别名的命令中包含 `$` 符号时，即认为使用了参数。**\n\n**此时，别名之后的内容会以参数方式解析，而不仅仅是替换别名**\n\n使用 [expandvars](https://github.com/sayanarijit/expandvars) 来解析参数，可实现参数默认值、切片等功能：\n\n- `alias test="echo ${1:-default}"`\n- `alias test="echo ${1:0:4}"`\n\n由于 expandvars 还未实现 shell 所有的变量扩展特性，具体可用的功能可以查看该项目\n\n### 传参示例\n\n<div align="left">\n<img src="./examples/3.png" width="500" />\n<img src="./examples/4.png" width="500" />\n</div>\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-alias',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
