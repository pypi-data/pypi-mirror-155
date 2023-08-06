#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
@Author  : ZuoXiang
@Email   : zx_data@126.com
@Time    : 2021/12/30 5:47 下午
@File    : setup.py
@Desc    : 
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jss_upload",
    version="0.1.3",
    author="zuoxiang",
    author_email="zx_data@126.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zuoxiang95/jss_upload",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
