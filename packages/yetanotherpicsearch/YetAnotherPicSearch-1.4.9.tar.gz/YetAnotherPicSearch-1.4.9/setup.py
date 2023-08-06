# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['YetAnotherPicSearch']

package_data = \
{'': ['*']}

install_requires = \
['PicImageSearch>=3.3.4,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'arrow>=1.2.0,<2.0.0',
 'lxml>=4.8.0,<5.0.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot2>=2.0.0b1,<3.0.0',
 'pyquery>=1.4.3,<2.0.0',
 'tinydb>=4.6.1,<5.0.0',
 'yarl>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'yetanotherpicsearch',
    'version': '1.4.9',
    'description': 'Yet Another Picture Search Nonebot Plugin',
    'long_description': '<div align="center">\n\n# YetAnotherPicSearch\n\n基于 [nonebot2](https://github.com/nonebot/nonebot2) 及 [PicImageSearch](https://github.com/kitUIN/PicImageSearch) 的另一个 Nonebot 搜图插件\n\n</div>\n\n## 简介\n\n主要受到 [cq-picsearcher-bot](https://github.com/Tsuk1ko/cq-picsearcher-bot) 的启发。 而我只需要基础的搜图功能，于是忍不住自己也写了一个。\n\n目前支持的搜图服务：\n\n- [saucenao](https://saucenao.com)\n- [whatanime](https://trace.moe)\n- [ascii2d](https://ascii2d.net)\n- [exhentai](https://exhentai.org)\n\n详细说明请移步：[文档](docs)\n\n目前适配的是 `OneBot V11` ，没适配 QQ 频道。\n\n## 感谢以下项目或服务（不分先后）\n\n- [saucenao](https://saucenao.com)\n- [ascii2d](https://ascii2d.net)\n- [trace.moe](https://trace.moe) ([GitHub](https://github.com/soruly/trace.moe))\n- [exhentai](https://exhentai.org)\n- [cq-picsearcher-bot](https://github.com/Tsuk1ko/cq-picsearcher-bot)\n- [PicImageSearch](https://github.com/kitUIN/PicImageSearch)\n',
    'author': 'NekoAria',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NekoAria/YetAnotherPicSearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
