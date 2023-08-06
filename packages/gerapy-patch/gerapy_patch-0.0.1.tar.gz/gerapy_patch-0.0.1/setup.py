from os.path import dirname, join
import io,os
from pkg_resources import parse_version
from setuptools import setup, find_packages, __version__ as setuptools_version
import sys



setup(
    name='gerapy_patch',
    version="0.0.1",
    url='https://scrapy.org',
    description="fix gerapy build egg can't pack cfg/xlsx/txt etc type files",
    author='buliqioqiolibusdo',
    author_email = 'dingyeran@163.com',
    license='BSD',
    packages=find_packages(exclude=('gereapy_patch-0.0.1.dist-info')),
    python_requires='>=3.6',
)
