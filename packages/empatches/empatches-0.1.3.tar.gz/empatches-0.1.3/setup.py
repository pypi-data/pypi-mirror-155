# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = "Extract and Merge image patches for easy, fast and self-contained digital image processing and deep learning model training."

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
INSTALL_REQUIRES = [
                    'numpy'
                    ]
# Setting up
setup(

        name="empatches", 
        version=VERSION,
        author="Talha Ilyas",
        LICENSE = 'MIT License',
        author_email="mr.talhailyas@gmail.com",
        description=DESCRIPTION,
        long_description= long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES, 
        
        url = 'https://github.com/Mr-TalhaIlyas/EMPatches',
        
        keywords=['python', 'extract image patches', 'merge image patches', 
                  'patchify', 'sliding window'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)