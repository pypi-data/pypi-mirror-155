# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_auto_teenstudy',
 'nonebot_plugin_auto_teenstudy.resource.crawl']

package_data = \
{'': ['*'],
 'nonebot_plugin_auto_teenstudy': ['data/*',
                                   'resource/*',
                                   'resource/dxx_bg/*',
                                   'resource/endpic/*',
                                   'resource/font/*',
                                   'resource/images/*',
                                   'resource/own_bg_hb/*']}

install_requires = \
['Pillow',
 'anti_useragent>=1.0.7,<1.1.0',
 'beautifulsoup4>=4.10.0,<4.11.0',
 'httpx>=0.20.0,<0.21.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot2>=2.0.0b2']

setup_kwargs = {
    'name': 'nonebot-plugin-auto-teenstudy',
    'version': '0.1.2',
    'description': '基于nonebot异步框架的青年大学自动提交插件',
    'long_description': '<div align="center">\n    <img src="https://s4.ax1x.com/2022/03/05/bw2k9A.png" alt="bw2k9A.png" border="0"/>\n    <h1>nonebot_plugin_auto_teenstudy</h1>\n    <b>基于nonebot2的青年大学习自动提交插件，用于自动完成大学习，在后台留下记录，返回完成截图</b>\n    <br/>\n    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>\n    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>\n    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>\n    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>\n</div>\n\n\n## 各地区使用方式（已经支持地区）\n\n- [江西地区](./nonebot_plugin_auto_teenstudy/resource/江西地区.md)\n- [湖北地区](./nonebot_plugin_auto_teenstudy/resource/湖北地区.md)\n\n## 已抓包分析但机器人不支持使用的地区请前往另一个仓库\n- [点我去另一个仓库](https://github.com/ZM25XC/commit_dxx)\n\n## 参考\n\n- [江西共青团自动提交](https://github.com/XYZliang/JiangxiYouthStudyMaker)\n\n- [青春湖北自动提交](https://github.com/Samueli924/TeenStudy)\n\n- [28位openid随机生成和抓包](https://hellomango.gitee.io/mangoblog/2021/09/26/other/%E9%9D%92%E5%B9%B4%E5%A4%A7%E5%AD%A6%E4%B9%A0%E6%8A%93%E5%8C%85/)\n- [定时推送大学习答案，完成截图](https://github.com/ayanamiblhx/nonebot_plugin_youthstudy)\n##  安装及更新\n\n1. 使用`git clone https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy.git`指令克隆本仓库或下载压缩包文件\n2. 使用`pip install nonebot-plugin-auto-teenstudy`来进行安装,使用`pip install nonebot-plugin-auto-teenstudy -U`进行更新\n\n## 导入插件\n**使用第一种安装方式**\n\n- 将`nonebot_plugin_auto_teenstudy`放在nb的`plugins`目录下，运行nb机器人即可\n\n**使用第二种安装方式**\n- 在`bot.py`中添加`nonebot.load_plugin("nonebot_plugin_auto_teenstudy")`或在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["nonebot_plugin_auto_teenstudy"]`\n\n\n## 机器人配置\n\n- 在nonebot的.env配置文件中设置好超管账号\n\n  ```py\n  SUPERUSERS=[""]\n  ```\n\n\n- 请确保已安装以下第三方库（插件运行失败请检查第三方库有没有装完整）\n\n  ```py\n  asyncio \n  anti_useragent \n  secrets\n  httpx\n  string\n  bs4\n  PIL\n  ```\n\n  \n\n## 功能列表\n\n### 大学习\n\n```py\n一、主人专用\n1、添加大学习配置|添加大学习用户|add_dxx\n指令格式：添加大学习配置#QQ号#地区#姓名#学校#团委(学院)#团支部(班级)\n2、删除大学习配置|删除大学习用户|del_dxx\n指令格式：删除大学习配置#QQ号\n3、查看大学习用户列表\n4、查看大学习用户|查看大学习配置|check_dxx_user\n指令格式：查看大学习用户#QQ号\n5、完成大学习|finish_dxx\n指令格式：完成大学习#QQ号\n6、添加（删除）推送好友\n指令格式：添加推送好友#QQ号\n7、添加（删除）推送群聊\n指令格式：添加（删除）推送群聊#群号\n8、查询推送好友（群聊）列表\n9、全局开启（关闭）大学习推送\n10、大学习图片回复开（关）|开启（关闭）大学习图片回复\n二、全员可用\n1、提交大学习\n2、我的大学习|查看我的大学习|my_dxx\n3、大学习功能|大学习帮助|dxx_help\n4、大学习|青年大学习\n5、大学习完成截图|完成截图|dxx_end\n6、设置大学习配置|set_dxx\n指令格式：设置大学习配置#地区#姓名#学校#团委(学院)#团支部(班级)\n7、个人信息截图|青春湖北截图（此功能只支持湖北用户）\n8、查组织|查班级|check_class\n指令格式：查组织#地区简写(例江西为：jx)#学校名称#团委名称\nPs:查组织功能对湖北用户无效！\n```\n\n## To Do\n- [ ] 增加ip池，防止多次用同一ip导致封ip\n- [ ] 增加更多地区支持\n- [ ] 优化 Bot\n- [ ] ~~逐步升级成群管插件~~\n\n## 更新日志\n\n### 2022/06/16\n\n- 因浙江地区一个openid只能提交一个人的大学习，故移除对浙江地区支持。\n- 将不支持使用机器人替多人完成大学习的地区的提交文件上传到另一[仓库](https://github.com/ZM25XC/commit_dxx)，单人使用可前往另一个[仓库](https://github.com/ZM25XC/commit_dxx)进行使用\n- 添加自动检查青年大学习更新并推送功能\n- 添加获取最新一期青年大学习答案和完成截图功能，完成截图功能有手机状态栏，状态栏时间会变。\n- 湖北地区增加获取个人信息截图功能。\n- 增加图片回复功能。\n### 2022/06/05\n\n- 增加浙江地区\n- 将爬取[江西](./nonebot_plugin_auto_teenstudy/resource/crawl/crawjx.py)和[浙江](./nonebot_plugin_auto_teenstudy/resource/crawl/crawlzj.py)地区高校团支部数据（抓取nid）文件上传\n### 2022/06/04\n\n- 将代码上传至pypi，可使用`pip install nonebot-plugin-auto-teenstudy`指令安装本插件\n- 增加已支持地区使用提示\n- 上传基础代码\n- 支持江西和湖北地区自动完成大学习（可在后台留记录）返回完成截图',
    'author': 'ZM25XC',
    'author_email': '2393899036@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
