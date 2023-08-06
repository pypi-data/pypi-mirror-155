# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 18:07:05 2022
@author:
Зайцева Дарья
"""

from setuptools import setup, find_packages
long_description= '''Library for the 3 semester'''
setup(name='scupy',
      version='0.0.10',
      url='https://github.com/dashkazaitseva',
      packages=find_packages(),
      license='MIT',
      description='',
      zip_safe=False,
      package_data={'scupy': ['.scupy/tasks_base.json']},
      include_package_data=True
      )