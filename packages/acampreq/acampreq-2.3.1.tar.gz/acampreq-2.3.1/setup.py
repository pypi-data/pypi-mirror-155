# -*- coding: utf-8 -*-

from setuptools import setup,find_packages

setup(
    name="acampreq",
    description="给A营用户的爬虫项目",
    long_description='''这是提供给A营用户的post项目(可以post用户,工作室,任务,作品)

至少使用2.0版本！远古版本可能含有严重bug！

-----

2.3更新日志

加入cookie

2.2更新日志

修复2.1版本的bug

2.1更新日志

让解码失败的提示更加友好，已知bug：req_iab.request.getOrPost函数返回值未使用。版本2.2将会修复该bug。

1.3更新日志

修复了一个中文错误

1.2更新日志

修复顽固bug（移除了him？）

1.1更新日志

修复了一个错误，完成了作品post

0.5.2更新日志

修复了一个中文错误  

0.5.1更新日志  

重新撰写了dsp和lgdsp  

0.5更新日志  

又更新了，完成了任务  

0.4更新日志  

大更新，完成了工作室post  

0.3.2更新日志  

再次修复了0.3.0中复发的bug  

0.3.1更新日志  

修补了另一个bug，可以正常使用了  

0.3.0更新日志  

修补bug！很重要！ 

0.2.3更新日志  

毫无存在感的更新  

0.2.2更新日志  

更新了函数  

0.2.1更新日志  

取消了Response 200的显示，修改了Response 404的显示，修复了一个bug，删去了类型输入提示，删去了showAbstract为N或n时的输出  
''',
    author="I_am_back",
    author_email="2682786816@qq.com",
    version="2.3.1",
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
