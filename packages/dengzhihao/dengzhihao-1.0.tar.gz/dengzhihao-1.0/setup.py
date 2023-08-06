from distutils.core import setup

setup(
    name='dengzhihao',	# 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦',	#描述
    author='dengzhihao', # 作者
    author_email='dengzhihao@163.com',
    py_modules=['dengzhihao.demo1','dengzhihao.demo2'] # 要发布的模块
)
