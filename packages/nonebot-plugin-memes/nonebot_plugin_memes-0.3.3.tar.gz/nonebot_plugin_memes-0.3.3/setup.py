# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_memes']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'httpx>=0.19.0',
 'imageio>=2.12.0,<3.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-imageutils>=0.1.6,<0.2.0',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-memes',
    'version': '0.3.3',
    'description': 'Nonebot2 plugin for making memes',
    'long_description': '# nonebot-plugin-memes\n\n[Nonebot2](https://github.com/nonebot/nonebot2) 插件，用于表情包制作\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n支持的表情包：\n\n发送“表情包制作”显示下图的列表：\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/06/14/wOLCQF8gxvm5lIc.jpg" width="500" />\n</div>\n\n\n#### 字体和资源\n\n插件使用 [nonebot-plugin-imageutils](https://github.com/noneplugin/nonebot-plugin-imageutils) 插件来绘制文字，字体配置可参考该插件的说明\n\n插件在启动时会检查并下载图片资源，初次使用时需等待资源下载完成\n\n可以手动下载 `resources` 下的 `images` 和 `thumbs` 文件夹，放置于机器人运行目录下的 `data/memes/` 文件夹中\n\n可以手动下载 `resources` 下 `fonts` 中的字体文件，放置于 nonebot-plugin-imageutils 定义的字体路径，默认为机器人运行目录下的 `data/fonts/` 文件夹\n\n\n### 示例\n\n - `/鲁迅说 我没说过这句话`\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/06/12/dqRF8egWb3U6Vfz.png" width="250" />\n</div>\n\n\n - `/举牌 aya大佬带带我`\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/06/12/FPuBosEgM3Qh1rJ.jpg" width="250" />\n</div>\n\n\n### 特别感谢\n\n- [Ailitonia/omega-miya](https://github.com/Ailitonia/omega-miya) 基于nonebot2的qq机器人\n\n- [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) 基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库，非常可爱的绪山真寻bot\n\n- [kexue-z/nonebot-plugin-nokia](https://github.com/kexue-z/nonebot-plugin-nokia) 诺基亚手机图生成\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MeetWq/nonebot-plugin-memes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
