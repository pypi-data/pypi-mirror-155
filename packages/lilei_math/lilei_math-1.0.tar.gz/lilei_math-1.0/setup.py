from distutils.core import setup

setup(
    name='lilei_math', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='lilei', # 作者
    author_email='gaoqi110@163.com',
    py_modules=['lilei_math.demo1','lilei_math.demo2'] # 要发布的模块

)