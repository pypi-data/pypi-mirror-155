# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_chatrecorder']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-datastore>=0.3.0,<0.4.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'sqlmodel>=0.0.6,<0.0.7',
 'typing-extensions>=3.10.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-chatrecorder',
    'version': '0.1.6',
    'description': '适用于 Nonebot2 的聊天记录插件',
    'long_description': "## nonebot-plugin-chatrecorder\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的聊天记录插件。\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_chatrecorder\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_chatrecorder\n```\n\n\n### 配置\n\n插件会记录机器人收到的消息，可以添加以下配置选择是否记录机器人发出的消息（默认为 `true`）；如果协议端开启了自身消息上报则需设置为 `false` 以避免重复\n\n```\nchatrecorder_record_send_msg=true\n```\n\n\n插件依赖 [nonebot-plugin-datastore](https://github.com/he0119/nonebot-plugin-datastore) 插件\n\n消息记录文件存放在 nonebot-plugin-datastore 插件设置的数据目录；同时插件会将消息中 base64 形式的图片、语音等存成文件，放置在 nonebot-plugin-datastore 插件设置的缓存目录，避免消息记录文件体积过大\n\n\n### 使用\n\n示例：\n\n```python\nfrom datetime import datetime, timedelta\nfrom nonebot_plugin_chatrecorder import get_message_records\nfrom nonebot.adapters.onebot.v11 import GroupMessageEvent\n\n@matcher.handle()\ndef handle(event: GroupMessageEvent):\n    # 获取当前群内成员 '12345' 和 '54321' 1天之内的消息\n    msgs = await get_message_records(\n        user_ids=['12345', '54321'],\n        group_ids=[event.group_id],\n        time_start=datetime.utcnow() - timedelta(days=1),\n    )\n```\n\n详细参数及说明见代码注释\n\n\n### TODO\n\n - 咕?\n - 咕咕咕！\n",
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MeetWq/nonebot-plugin-chatrecorder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
