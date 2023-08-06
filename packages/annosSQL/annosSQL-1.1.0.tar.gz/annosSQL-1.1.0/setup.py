import pathlib
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

# 发布在pip上的说明文档
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='annosSQL', # 包名
    version='1.1.0', # 包版本
    description='python for mysql operation', # 包简单描述
    long_description=long_description, # 包长描述
    long_description_content_type='text/markdown', # 包长描述格式
    url='https://gitee.com/chx516/annosSQL',  # 包地址
    author='czh', # 作者
    author_email='utowe@qq.com', # 作者邮件
    license='MIT', # 协议
    keywords='python annos', # 关键词
    packages=[ # 公开的子包
        'annosSQL.Donos',
        'annosSQL.Innos',
        'annosSQL.test',
    ],
    install_requires=['pymysql'], # 依赖
    python_requires='>=3' # python版本依赖
)
