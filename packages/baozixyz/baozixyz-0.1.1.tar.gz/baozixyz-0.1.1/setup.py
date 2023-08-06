# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    # 指定项目名称，我们在后期打包时，这就是打包的包名称，当然打包时的名称可能还会包含下面的版本号哟~
    name='baozixyz',
    version='0.1.1',
    description='Python automatic operation and maintenance platform',
    packages=find_packages()
)
