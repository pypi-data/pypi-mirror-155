# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Kuture
# Mail: kuture@163.com
# Blog: http://www.kuture.com.cn
# Created Time:  2020-7-8 12:00:00
#############################################


from setuptools import setup, find_packages

with open("README.md", 'r') as rf:
    long_description = rf.read()

setup(
    name="akstatistic",
    version="0.0.2",
    keywords=["pip", "akstatistic", "aktools", "kuture", "statistic"],
    description="Project Code Statistic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://gitee.com/aktools/akstatistic.git",
    author="Kuture",
    author_email="kuture@163.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],
    python_requires=">=3",
)
