# -*- coding: utf-8 -*-
# Author: Runsheng Xu <rxx3386@ucla.edu>
# License: TDG-Attribution-NonCommercial-NoDistrib


from os.path import dirname, realpath
from setuptools import setup, find_packages, Distribution
from opencood.version import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='opencoodx',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/ucla-mobility/OpenCDA.git',
    license='MIT',
    author='Runsheng Xu, Hao Xiang, Zhaoliang Zheng',
    author_email='rxx3386@ucla.edu,zhz03@g.ucla.edu',
    description='An opensource pytorch framework for autonomous driving '
                'cooperative detection',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "matplotlib",
        "numpy",
        "open3d",
        "opencv-python",
        "cython",
        "tensorboardX",
        "shapely",
        "einops",
        "easydict",
        "gdown"
        ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["opencoodx=opencood.cood:main"]},
)
