# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_shindan']

package_data = \
{'': ['*'], 'nonebot_plugin_shindan': ['templates/*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'beautifulsoup4>=4.0.0,<5.0.0',
 'httpx>=0.19.0',
 'lxml>=4.0.0,<5.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-htmlrender>=0.0.4',
 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-shindan',
    'version': '0.2.3.1',
    'description': 'Nonebot2 plugin for using ShindanMaker',
    'long_description': '# nonebot-plugin-shindan\n\n使用 [ShindanMaker](https://shindanmaker.com) 网站的~~无聊~~趣味占卜\n\n利用 playwright 将占卜结果转换为图片发出，因此可以显示图片、图表结果\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_shindan\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_shindan\n```\n\n插件依赖 [nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender) 插件来渲染图片，使用前需要检查 playwright 相关的依赖是否正常安装；同时为确保字体正常渲染，需要系统中存在中文字体\n\n\n### 使用方式\n\n默认占卜列表及对应的网站id如下：\n\n- 今天是什么少女 (162207)\n- 人设生成 (917962)\n- 中二称号 (790697)\n- 异世界转生 (587874)\n- 特殊能力 (1098085)\n- 魔法人生 (940824)\n- 抽老婆 (1075116)\n- 抽舰娘 (400813)\n- 抽高达 (361845)\n- 英灵召唤 (595068)\n- 选秀剧本 (1098152)\n- 卖萌 (360578)\n\n发送 “占卜指令 名字” 即可，如：`人设生成 小Q`\n\n发送 “/占卜列表” 可以查看上述列表；\n\n超级用户可以发送 “/添加占卜 id 指令”、“/删除占卜 id” 增删占卜列表，可以发送 “/设置占卜 id image/text”设置输出形式\n\n对于需要登录推特的占卜，可以在 `.env.xxx` 文件中添加 ShindanMaker cookie：\n\n```\nshindanmaker_cookie=xxx\n```\n\n`cookie` 获取方式：\n\n`F12` 打开开发工具，查看 `shindanmaker.com` 请求的响应头，找形如 `_session=xxx;` 的片段\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/06/18/1CqlcTrdVt5vJp6.png" width="500" />\n</div>\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MeetWq/nonebot-plugin-shindan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
