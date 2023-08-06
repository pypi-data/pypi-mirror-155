from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


install_requires = ['requests>=2.25.1']


setup(
name='OpenAnnotatePy',
version='0.0.1', 
author='Gaozj',
author_email='3193346402@qq.com',
url='https://github.com/ZjGaothu/OpenAnnotatePy',
description='A python package for efficiently annotating the chromatin accessibility of genomic regions.',
long_description=long_description,
long_description_content_type= 'text/markdown',
packages=find_packages(),
install_requires=install_requires,
license = 'Apache License 2.0',
project_urls={ 
        'Web': 'http://health.tsinghua.edu.cn/openannotate',
    })