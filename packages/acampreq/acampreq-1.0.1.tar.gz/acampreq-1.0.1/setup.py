from distutils.core import setup
VERSION = "1.0.1"

setup(
    name="acampreq",
    description="给A营用户的爬虫项目",
    author="I_am_back",
    author_email="2682786816@qq.com",
    version=VERSION,
    long_description="给A营用户的爬虫项目(爬取作品或爬取用户)",
    long_description_content_type="markdown",
    install_requires=[
        "requests>=2.6.0",
        "json>=2.0.9",
        "req_iab>=1.0.5",
    ],
    
)
