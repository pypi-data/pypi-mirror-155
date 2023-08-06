# -*- coding: utf-8 -*-

from setuptools import setup,find_packages

setup(
    name="acampreq",
    description="给A营用户的爬虫项目",
    long_description='''这是提供给A营用户的post项目(可以post用户,工作室,任务,作品)。

至少使用2.0版本！远古版本可能含有严重bug！''',
    author="I_am_back",
    author_email="2682786816@qq.com",
    version="2.4",
    url="https://pypi.org",
    install_requires=[
        "req_iab>=1.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Development Status :: 6 - Mature",
    ],
    packages=find_packages(),
)
