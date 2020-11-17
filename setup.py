# -*- coding: utf-8 -*-
'''
Setup file
'''
import os
import setuptools

setup_dir = os.path.dirname(__file__)
with open(os.path.join(setup_dir, 'XSteamPython', '__init__.py'), 'w') as init:
    init.write('from .XSteamPython import *')

with open(os.path.join(setup_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='XSteamPython', \
    version='1.0.1', \
    description='Port of XSteam tables by Magnus Holmgren to python', \
    long_description=long_description, \
    long_description_content_type='text/markdown', \
    url='https://github.com/raldridge11/XSteamPython', \
    author='Magnus Holmgren; ported by R. Aldridge', \
    packages=setuptools.find_packages(), \
    python_requires='>=2.7, >=3.4.*', \
    install_requires=['scipy==1.2.1'], \
    classifiers=['License :: OSI Approved :: GNU General Public License v2 (GPLv2)', \
        'Programming Language :: Python :: 2.7', \
        'Programming Language :: Python :: 3.4', \
        'Programming Language :: Python :: 3.5', \
        'Programming Language :: Python :: 3.6', \
        'Programming Language :: Python :: 3.7']
)

os.remove(os.path.join(setup_dir, 'XSteamPython', '__init__.py'))