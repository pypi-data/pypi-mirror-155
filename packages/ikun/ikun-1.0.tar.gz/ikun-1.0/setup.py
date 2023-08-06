# -*- coding: UTF-8 -*-
from distutils.core import setup
setup(
    name='ikun',# 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦',	#描述
    author='joker', # 作者
    author_email='lsc_1219@163.com',
    py_modules=['ikun.demo1','ikun.demo2'] # 要发布的模块
)