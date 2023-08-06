# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_caiyunai']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-imageutils>=0.1.6,<0.2.0',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-caiyunai',
    'version': '0.2.3',
    'description': '适用于 Nonebot2 的彩云小梦AI续写插件',
    'long_description': '# nonebot-plugin-caiyunai\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的彩云小梦AI续写插件\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_caiyunai\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_caiyunai\n```\n\n\n### 配置\n\n需要在 `.env.xxx` 文件中添加彩云小梦apikey：\n\n```\ncaiyunai_apikey=xxx\n```\n\napikey获取：\n\n前往 http://if.caiyunai.com/dream 注册彩云小梦用户；\n\n注册完成后，F12打开开发者工具；\n\n在控制台中输入 `alert(localStorage.cy_dream_user)` ，弹出窗口中的 uid 即为 apikey；\n\n或者进行一次续写，在 Network 中查看 novel_ai 请求，Payload 中的 uid 项即为 apikey。\n\n\n### 使用\n\n#### 触发方式：\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n```\n@机器人 续写/彩云小梦 xxx\n```\n\n\n#### 示例：\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/01/15/zKcCMTehNOUxFJI.jpg" width="400" />\n  <img src="https://s2.loli.net/2022/01/15/R6HcEuN2gXmsDBJ.jpg" width="400" />\n</div>\n\n\n### 特别感谢\n\n- [assassingyk/novel_ai_kai](https://github.com/assassingyk/novel_ai_kai) 适用hoshino的基于彩云小梦的小说AI续写插件\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noneplugin/nonebot-plugin-caiyunai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
