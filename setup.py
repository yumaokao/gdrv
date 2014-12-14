#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

from setuptools import setup
from gdrv import global_mod as gm

setup(name='gdrv',
      version=gm.version,
      description='Another google drive command line interface program',
      url='https://github.com/yumaokao/gdrv',
      author='yumaokao',
      author_email='ymkq9h@gmail.com',
      license='MIT',
      packages=['gdrv', 'gdrv.commands'],
      entry_points={
          'console_scripts':
              ['gdrv = gdrv.main:main']
      },
      install_requires=[
          'google-api-python-client',
          'progressbar',
          'colorama'
      ],
      zip_safe=False)
