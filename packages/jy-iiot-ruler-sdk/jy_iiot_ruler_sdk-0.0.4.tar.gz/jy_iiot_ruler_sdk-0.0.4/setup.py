# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path

'''
    发布到pypi:
    pypi账号:feelingsray(feelingswl@gmail.com) Jykj1234
    conda activate jy-iiot-py
    python setup.py check
    python setup.py sdist bdist_egg bdist_wheel
    twine upload dist/*
'''

here = path.abspath(path.dirname(__file__))

setup(
    name='jy_iiot_ruler_sdk',
    version='0.0.4',
    author='RayWong',
    author_email='wanglei@jylink.com',
    description='精英物联网数据服务平台规则引擎轻代码开发SDK',
    #long_description=long_description,  # 这里是文档内容, 读取readme文件
    #long_description_content_type='text/markdown',  # 文档格式
    packages=find_packages(),
    classifiers=[  # 这里我们指定证书, python版本和系统类型
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        #"Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 这里指定python版本号必须大于3.6才可以安装
    install_requires=['requests']  # 我们的模块所用到的依赖, 这里指定的话, 用户安装你的模块时, 会自动安装这些依赖
)