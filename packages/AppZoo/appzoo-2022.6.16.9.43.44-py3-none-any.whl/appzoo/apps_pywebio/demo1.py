#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : demo1
# @Time         : 2022/6/2 下午1:57
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from pywebio.input import *


# 输入框
input_res = input("please input your name:")
print(type(input_res))
print('browser input is:', input_res)
