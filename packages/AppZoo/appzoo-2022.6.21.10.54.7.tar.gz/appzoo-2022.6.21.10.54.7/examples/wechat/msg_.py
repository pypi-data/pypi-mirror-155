#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : msg
# @Time         : 2022/6/7 下午4:21
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.str_utils import json_loads
from meutils.notice.wechat import WeChatClient

from appzoo import App

app = App()
app_ = app.app


def appchat_send_text(kwargs: str):
    kwargs = json_loads(kwargs)

    name = kwargs.get('name', 'Notice')
    agent_id = kwargs.get('agent_id', '1000002')
    content = kwargs.get('content', '这是一条测试文本')

    corp_id = 'wwc18433f3075302e4'
    secret = 'iL_8JXBoB5vFITCcOk2-EvP6TcOnVCjZI1LRw8vidtE'
    api_base_url = None

    if kwargs.pop('prd', None):  # 默认测试环境
        corp_id = 'ww3c6024bb94ecef59'
        secret = '6Q2qFXgGSpAWb31zeYNS-FEEvmOScEv4d4sCnAK2kcQ'
        api_base_url = 'https://qywxlocal.nesc.cn:7443/cgi-bin/'

    wc = WeChatClient(corp_id, secret, api_base_url)

    wc.appchat.send(wc.name2id(name), 'text', content=content)

    return 'ok'


def appchat_send_file(kwargs: dict):
    io = kwargs['files'][0]

    name = kwargs.get('name', 'Notice')
    agent_id = kwargs.get('agent_id', '1000002')

    corp_id = 'wwc18433f3075302e4'
    secret = 'iL_8JXBoB5vFITCcOk2-EvP6TcOnVCjZI1LRw8vidtE'
    api_base_url = None

    if kwargs.pop('prd', None):  # 默认测试环境
        name = kwargs.get('name')

        corp_id = 'ww3c6024bb94ecef59'
        secret = '6Q2qFXgGSpAWb31zeYNS-FEEvmOScEv4d4sCnAK2kcQ'
        api_base_url = 'https://qywxlocal.nesc.cn:7443/cgi-bin/'

    wc = WeChatClient(corp_id, secret, api_base_url)

    media_id = wc.media.upload('file', io)['media_id']  ####
    wc.appchat.send(wc.name2id(name), 'file', media_id=media_id)



app.add_route_plus(appchat_send_text)
app.add_route_uploadfiles('/appchat-send-file', appchat_send_file)

if __name__ == '__main__':
    # appchat_send(
    #     str(
    #         {
    #             'name': 'Notice',
    #             'msg_type': 'text',
    #             'msg_json': {
    #                 'content': '这是一条测试文本'
    #             }
    #         }
    #     ))  # text
    #
    #
    # appchat_send_file(
    #
    #         {
    #             'name': 'Notice',
    #             'files': [open('/Users/yuanjie/Desktop/111.jpeg', 'rb').read()]
    #         }
    #     )  # image


    app.run(app.app_from(__file__), port=8000, debug=True)
