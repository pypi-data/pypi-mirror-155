#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : main
# @Time         : 2022/6/14 下午2:01
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 



from meutils.pipe import *
from appzoo import App

app = App()
app_ = app.app


# app.add_route('/get', lambda **kwargs: kwargs, method="GET", result_key="GetResult")
# app.add_route('/post', lambda **kwargs: kwargs, method="POST", result_key="PostResult")
#
# app.add_route_plus('/post_test', lambda **kwargs: kwargs, method="POST")
#
# from fastapi import FastAPI, Form, Depends, File, UploadFile, Body, Request, Path
#
# def proxy_app_(kwargs: dict):
#     logger.info(kwargs)
#     print(kwargs)
#     r = requests.request(**kwargs)
#     return r.json()
#
#
# app.add_route_plus(proxy_app_, methods=["GET", "POST"], data=None)

if __name__ == '__main__':
    # app.run(app.app_from(__file__), port=9955, debug=True)

    app.gunicorn_run()
