#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
        long_description = readme.read()
except:
    long_description = ""

setup(name='compscifirebaselite',
      version='1.0.0',
      description='Computer Science Firebase Package which is a lite version for python-firebase',
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.2',
          'Natural Language :: English',
      ],
      keywords='firebase python',
      author='Eoin Gallen',
      author_email='egallen@sainteunans.com',
      url='https://github.com/MrGallen/firebase-compsci',
      license='MIT',
      packages=['compscifirebaselite'],
      test_suite='tests.all_tests',
      install_requires=['requests>=1.1.0'],
      zip_safe=False,
)
