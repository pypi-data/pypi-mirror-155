from setuptools import setup, find_packages
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


long_desc = """
todo
"""


def read_install_requires():
    reqs = [
        'requests',
        'pandas'
    ]
    return reqs


setup(
    name='taodata',
    version='0.1.13',
    description='todo',
    long_description=long_desc,
    author='Daniel Qian',
    author_email='909263817@qq.com',
    license='MIT',
    url='https://taodata.pro',
    install_requires=read_install_requires(),
    keywords='todo',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.csv', '*.txt']},
)