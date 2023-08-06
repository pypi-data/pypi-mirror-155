# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:50:35 2022

@author: Jinhai
"""

from setuptools import setup, find_packages

VERSION = '0.1.1' 
DESCRIPTION = 'Digital Simulation for Neural Networks'
LONG_DESCRIPTION = 'A simulation package for neural network on digital hardwares'

# Setting up
setup(
   # the name must match the folder name 'verysimplemodule'
    name = "DigiNet", 
    version = VERSION,
    author = "Jinhai Hu",
    author_email = "<jinhai001@e.ntu.edu.sg>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], # add any additional packages that 
    # needs to be installed along with your package. Eg: 'caer'
    
    keywords=['python', 'Digital Hardwares', 'Neural Networks'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)