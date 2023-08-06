# coding:utf-8
"""Setup Script for MDCLogger"""
import warnings
from distutils.core import setup
from sys import version_info

py_version = version_info[:2]
if not (2, 6) <= py_version <= (2, 7) and not (3, 4) <= py_version < (4, 0):
    raise ImportError('Python %d.%d is not supported by MDCLogger.' % py_version)

warnings.filterwarnings('ignore', 'Unknown distribution option')

__version__ = '0.8'

readme = open('README.rst').read()

setup(
    name='MDCLogger',  # 模块名
    version=__version__,  # 版本号 这里决定了发布到pypi上的版本号
    description='one collection log extension tools ',  # 标题描述
    long_description=readme,  # 说明
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    author='zhang zixiao',
    author_email='zhangzixiao@189.cn',
    maintainer='zhang zixiao',
    maintainer_email="zhangzixiao@189.cn",
    url='https://gitee.com/ctec/CDBUtils',
    platforms=['any'],
    license='MIT License',
    packages=['MDCLogger', 'MDCLogger.Tests'],
    package_data={'MDCLogger': ['Tests/*']}
)
