# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_arcaeabot',
 'nonebot_plugin_arcaeabot.api',
 'nonebot_plugin_arcaeabot.handler',
 'nonebot_plugin_arcaeabot.message',
 'nonebot_plugin_arcaeabot.message.image_message',
 'nonebot_plugin_arcaeabot.message.image_message.best_30',
 'nonebot_plugin_arcaeabot.message.image_message.single_song',
 'nonebot_plugin_arcaeabot.message.text_message',
 'nonebot_plugin_arcaeabot.schema',
 'nonebot_plugin_arcaeabot.schema.v5']

package_data = \
{'': ['*'],
 'nonebot_plugin_arcaeabot': ['resource/b30/*',
                              'resource/diff/*',
                              'resource/font/*',
                              'resource/grade/*',
                              'resource/ptt/*',
                              'resource/recent/*']}

install_requires = \
['Pillow>=8.3.1',
 'httpx>=0.20.0,<1.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<=2.1.0',
 'nonebot2>=2.0.0-beta.1,<=2.0.0-beta.3',
 'peewee>=3.14.4',
 'ruamel.yaml>=0.17.2,<0.18.0',
 'tqdm>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-arcaeabot',
    'version': '3.0.1',
    'description': 'An arcaea plugin for nonebot2. ( A cross platform Python async bot framework. )',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://s2.loli.net/2022/06/16/opBDE8Swad5rU3n.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-arcaeabot\n\n_✨ Arcaea查分插件 ✨_\n</div>\n\n\n## 功能 Resume\n\nArcaea 查分器。\n\n使用 /arc help查看帮助信息\n\n[更新日志](https://github.com/SEAFHMC/nonebot-plugin-arcaeabot/blob/v3.0.0/CHANGELOG.MD)\n\n## 如何开始 Quick Start\n\n***请注意! 您需要填写相关配置才能正常使用***\n\n使用前请确保您的Python版本>=3.8\n\n项目默认使用AUA (ArcaeaUnlimitedApi)，您需要申请相关apiurl与token(user-agent)并在机器人所在目录`data\\arcaea\\config.yml`中填写\n\n<div align="center">\n\n| 参数               | 描述                                                         |\n| ------------------ | ------------------------------------------------------------ |\n| AUA_URL | AUA的地址，如"https://www.example.com"</br>（不需要添加/botarcapi） |\n| AUA_UA | AUA请求头User-Agent，如"Grievous Lady (Linux; U; Android 2.3.3; BotArcAPI)" |\n\n</div>\n\n使该项目被您的 NoneBot2 (nonebot2 及 nonebot-adapter-onebot 版本不得低于 `2.0.0-beta2` ) 机器人作为插件加载, 至于如何做, 您应该懂的。\n\n### 首次使用您需要更新资源文件(assets/song, assets/char)\n\n- 向bot发送"/arc assets_update"以更新资源文件。\n- 如果更新失败（资源更新服务器炸了）您可以使用[ArcaeaAssetsUpdater](https://github.com/SEAFHMC/ArcaeaAssetsUpdater)搭建自己的资源更新服务器，然后在 config.yml 中填写您的api地址)\n- 还可以直接从[百度云](https://pan.baidu.com/s/1rR5NOy1zSeHIGZ97oNElTQ?pwd=c4iv)下载资源文件（更新至3.12.10c），并放置于bot目录/data/arcaea/assets中\n\n## 指令 Command\n\n<div align="center">\n\n| 指令                                        | 描述                                                              |\n| ------------------------------------------- | ------------------------------------------------------------      |\n| /arc assets_update                          | 更新曲绘, 请务必在您初次使用该插件或者 Arcaea 版本有更新时发送此命令   |\n| /arc help                                   | 查看该插件的帮助文档                                                |\n| /arc bind {id}                              | 绑定您的 Arcaea 账户, 可以是id也可以是用户名                          |\n| /arc info                                   | 查询您的绑定信息                                                   |\n| /arc recent                                 | 查询您的最近游玩信息                                               |\n| /arc b30                                    | 查询您的 best 30 记录                                              |\n| /arc best {songname} {difficulty}           | 查询您的单曲最佳记录                                               |\n| /arc song {songname} {difficulty}           | 查询歌曲信息                                                       |\n| /arc random {start} {end} {difficulty}      | 随机歌曲                                                          |\n| /arc preview {songname} {difficulty}         | 查询歌曲谱面预览                                                          |\n\n</div>\n  \n## To Do\n- 咕咕咕\n\n## 感谢\n\n- [Awbugl/Andreal](https://github.com/Awbugl/Andreal)\n- [DiheChen/nonebot-plugin-arcaea](https://github.com/DiheChen/nonebot-plugin-arcaea)\n- [iyume/nonebot-plugin-arcaea](https://github.com/iyume/nonebot-plugin-arcaea)\n',
    'author': 'SEAFHMC',
    'author_email': 'soku_ritsuki@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SEAFHMC/nonebot-plugin-arcaeabot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
