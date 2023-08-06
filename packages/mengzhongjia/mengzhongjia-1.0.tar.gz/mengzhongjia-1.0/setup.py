from distutils.core import setup

setup(

    name='mengzhongjia',  # 对外我们模块的名字

    version='1.0',  # 版本号

    description='这是第一个对外发布的模块，测试哦',  # 描述

    author='mzj',  # 作者

    author_email='mengzhongjia1113@163.com',

    py_modules=['mengzhongjia.demo1', 'mengzhongjia.demo2']  # 要发布的模块

)
