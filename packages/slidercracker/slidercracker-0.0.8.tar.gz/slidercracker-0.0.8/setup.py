#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="slidercracker",
    version="0.0.8",
    author="ZeroSeeker",
    author_email="zeroseeker@foxmail.com",
    description="make it easy to crack slider",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://gitee.com/ZeroSeeker/slidercracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'easydownload==0.0.1',
        'numpy==1.22.0',
        'opencv-python==4.5.5.64',
        'requests==2.27.1'
    ]
)
