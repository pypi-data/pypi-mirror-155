from distutils.core import setup

setup(

   name='kunkun',	# 对外我们模块的名字

   version='1.0', # 版本号

   description='这是第一个对外发布的模块，测试哦',	#描述

   author='gaoqi', # 作者

   author_email='gaoqi110@163.com',

   py_modules=['kunkun.demo1','kunkun.demo2'] # 要发布的模块

)