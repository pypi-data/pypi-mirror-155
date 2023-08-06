#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : __init__.py
# @Time         : 2022/3/24 上午11:08
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *





a = yaml_load('/Users/yuanjie/Desktop/Projects/Python/AppZoo/examples/wechat/url.yml')





from pprint import pprint
pprint(a)


#
# from meutils.notice.wechat import WeChatClient
# WeChatClient(**a['wechat']['TEST']).appchat.send(1162363786, 'text')