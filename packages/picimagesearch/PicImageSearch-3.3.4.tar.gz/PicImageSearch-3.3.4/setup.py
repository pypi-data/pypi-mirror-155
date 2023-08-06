# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['PicImageSearch', 'PicImageSearch.model']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'lxml>=4.8.0,<5.0.0', 'pyquery>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'picimagesearch',
    'version': '3.3.4',
    'description': 'PicImageSearch APIs for Python 3.x 适用于 Python 3 以图搜源整合API',
    'long_description': '<div align="center">\n\n# PicImageSearch\n\n✨ 聚合识图引擎 用于以图搜源✨\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/kitUIN/PicImageSearch/master/LICENSE">\n    <img src="https://img.shields.io/github/license/kitUIN/PicImageSearch" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/PicImageSearch">\n    <img src="https://img.shields.io/pypi/v/PicImageSearch" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.6+-blue" alt="python">\n  <a href="https://github.com/kitUIN/PicImageSearch/releases">\n    <img src="https://img.shields.io/github/v/release/kitUIN/PicImageSearch" alt="release">\n  </a>\n  <a href="https://github.com/kitUIN/PicImageSearch/issues">\n    <img src="https://img.shields.io/github/issues/kitUIN/PicImageSearch" alt="release">\n  </a>\n </p>\n<p align="center">\n  <a href="https://www.kituin.fun/wiki/picimagesearch/">📖文档</a>\n  ·\n  <a href="https://github.com/kitUIN/PicImageSearch/issues/new">🐛提交建议</a>\n</p>\n\n## 支持\n- [x] [SauceNAO](https://saucenao.com/)\n- [x] [TraceMoe](https://trace.moe/)\n- [x] [Iqdb](http://iqdb.org/)\n- [x] [Ascii2D](https://ascii2d.net/)\n- [x] [Google谷歌识图](https://www.google.com/imghp)\n- [x] [BaiDu百度识图](https://graph.baidu.com/)\n- [x] [E-Hentai](https://e-hentai.org/)\n- [x] [ExHentai](https://exhentai.org/)\n- [x] 同步/异步\n## 简要说明\n\n详细见[文档](https://www.kituin.fun/wiki/picimagesearch/) 或者[`demo`](https://github.com/kitUIN/PicImageSearch/tree/main/demo)  \n`同步`请使用`from PicImageSearch.sync import ...`导入  \n`异步`请使用`from PicImageSearch import Network,...`导入  \n**推荐使用异步**  \n\n## 简单示例\n```python\nfrom loguru import logger\nfrom PicImageSearch.sync import SauceNAO\n\nsaucenao = SauceNAO()\nres = saucenao.search(\'https://pixiv.cat/77702503-1.jpg\')\n# res = saucenao.search(r\'C:/kitUIN/img/tinted-good.jpg\') #搜索本地图片\nlogger.info(res.origin)  # 原始数据\nlogger.info(res.raw)  #\nlogger.info(res.raw[0])  #\nlogger.info(res.long_remaining)  # 99\nlogger.info(res.short_remaining)  # 3\nlogger.info(res.raw[0].thumbnail)  # 缩略图\nlogger.info(res.raw[0].similarity)  # 相似度\nlogger.info(res.raw[0].title)  # 标题\nlogger.info(res.raw[0].author)  # 作者\nlogger.info(res.raw[0].url)\n```\n\n```python\nfrom PicImageSearch import SauceNAO, Network\n\nasync with Network() as client:  # 可以设置代理 Network(proxies=\'http://127.0.0.1:10809\')\n    saucenao = SauceNAO(client=client)  # client不能少\n    res = await saucenao.search(\'https://pixiv.cat/77702503-1.jpg\')\n    # 下面操作与同步方法一致\n```\n### 安装\n- 此包需要 Python 3.6 或更新版本。\n- `pip install PicImageSearch`\n- 或者\n- `pip install PicImageSearch -i https://pypi.tuna.tsinghua.edu.cn/simple`\n\n## Star History\n\n[![Star History](https://starchart.cc/kitUIN/PicImageSearch.svg)](https://starchart.cc/kitUIN/PicImageSearch)\n',
    'author': 'kitUIN',
    'author_email': 'kulujun@gmail.com',
    'maintainer': 'kitUIN',
    'maintainer_email': 'kulujun@gmail.com',
    'url': 'https://github.com/kitUIN/PicImageSearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
