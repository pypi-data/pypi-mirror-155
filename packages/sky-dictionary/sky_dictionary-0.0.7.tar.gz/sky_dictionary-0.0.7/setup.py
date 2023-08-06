# encoding: utf-8
"""
@project: djangoModel->setup
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 模块打包文件
@created_time: 2022/6/18 15:14
"""
from setuptools import setup

with open('README.md', 'r', encoding='utf8') as fp:
    log_desc = fp.read()

setup(
    name='sky_dictionary',  # 模块名称
    version='0.0.7',  # 模块版本
    description='字段配置模块',  # 段描述
    long_description=log_desc,
    long_description_content_type="text/markdown",
    author='sunkaiyan',
    author_email='sky4834@163.com',
    # packages=find_packages(),  # 系统自动从当前目录开始找包
    packages=['sky_dictionary'],  # 系统自动从当前目录开始找包
    license="apache 3.0",

    install_requires=[
        'django',
        'django_simple_api',
        'mysqlclient'
    ]
)
