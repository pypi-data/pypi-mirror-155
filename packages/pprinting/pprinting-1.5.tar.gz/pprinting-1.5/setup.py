# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pprinting',  # 模块名称
    version="1.5",  # 当前版本
    author="wd",  # 作者
    author_email="1572990942@qq.com",  # 作者邮箱
    description="字符串格式化输出对象",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://www.baidu.com",
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    # install_requires=[],
    python_requires='>=3.6',   # 其余的我懒得试了 报错自己改源码
)
