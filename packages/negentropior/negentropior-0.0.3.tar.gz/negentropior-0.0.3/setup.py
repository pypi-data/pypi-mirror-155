#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requires=['aliyun-python-sdk-core==2.13.36']

setup(name='negentropior',
      version='0.0.3',
      description='ILabor algorithm group tools 算法组常用工具方法',
      author='Yi OuYang, ZhiWen Wang',
      author_email='yiouyang143@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=requires,
)
