# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 18:07:05 2022
@author:
Зайцева Дарья
"""

from setuptools import setup, find_packages
long_description= '''Library for the 3 semester'''
setup(name='scupy',
      version='0.0.14',
      url='https://github.com/dashkazaitseva',
      packages=['scupy'],
      license='MIT',
      description='',
      zip_safe=False,
      package_data={'scupy': ['*.json']},
      include_package_data=True
      )