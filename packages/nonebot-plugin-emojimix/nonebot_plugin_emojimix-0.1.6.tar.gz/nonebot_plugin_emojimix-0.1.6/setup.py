# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_emojimix']

package_data = \
{'': ['*']}

install_requires = \
['emoji>=1.7.0,<2.0.0',
 'httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-emojimix',
    'version': '0.1.6',
    'description': 'Nonebot2 plugin for emojimix',
    'long_description': '# nonebot-plugin-emojimix\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的 emoji 合成器\n\n😎+😁=？\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_emojimix\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_emojimix\n```\n\n若经常下载出错，可以在 `.env.xxx` 文件中设置代理：\n\n```\nhttp_proxy=http://ip:port\n```\n\n\n### 示例\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/01/23/EyoA1BHe9YpJZUD.png" width="400" />\n</div>\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MeetWq/nonebot-plugin-emojimix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
