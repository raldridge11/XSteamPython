import os
from distutils.core import setup

open('__init__.py', 'a').close()

setup(name='XSteamPython',
      version='0.0.0',
      description='Steam Tables in Python',
      packages=['XSteamPython'],
     )

os.remove('__init__.py')