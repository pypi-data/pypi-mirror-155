#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : msg
# @Time         : 2022/6/7 下午4:21
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
from meutils.pipe import *
from meutils.notice.wechat import WeChatClient

from appzoo import App

app = App()
app_ = app.app
app.config = yaml_load(get_resolve_path('wechat.yml', __file__))


def appchat_send(kwargs):
    appid = kwargs.pop('appid', 'TEST')
    cfg = app.config['wechat']
    wc = WeChatClient(**cfg[appid])

    kwargs = {**{'chat_id': 1162363786, 'msg_type': 'text', 'content': '这是一条测试信息'}, **kwargs}
    msg_type = kwargs.get('msg_type', 'text')

    if msg_type == 'text':
        wc.appchat.send(**kwargs)

    elif msg_type in {'image', 'voice', 'file'}:
        for io in kwargs.pop('files'):
            kwargs['media_id'] = wc.media.upload(msg_type, io)['media_id']
            wc.appchat.send(**kwargs)

    return kwargs

app.add_route_plus(appchat_send, methods=['get', 'post'])

if __name__ == '__main__':
    app.run(app.app_from(__file__), port=8000, debug=True)
    # appchat_send({'appid': 'ai'})
