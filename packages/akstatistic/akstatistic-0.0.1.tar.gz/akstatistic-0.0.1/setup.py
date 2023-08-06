#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Kuture
# Mail: kuture@163.com
# Blog: http://www.kuture.com.cn
# Created Time:  2020-7-8 12:00:00
#############################################


from setuptools import setup, find_packages

setup(
    name = "akstatistic",
    version = "0.0.1",
    keywords = ("pip", "akstatistic", "aktools", "kuture", "statistic"),
    description = "Project Code Statistic",
    long_description = "用于统计项目中的代码行数，一共2个参数，filter_list：文件类型，默认为.py，\n"
                       "source_dir_path:要进行代码行数统计的项目，默认为当前运行路径\n。",

    license = "MIT Licence",

    url = "https://gitee.com/aktools/akstatistic",
    author = "Kuture",
    author_email = "kuture@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
