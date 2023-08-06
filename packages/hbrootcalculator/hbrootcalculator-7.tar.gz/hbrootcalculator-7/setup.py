from setuptools import setup, find_packages
import os

with open('README.md') as f:
    long_description = f.read()

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='hbrootcalculator',
  version='7',
  description='A VERY BASIC ROOT CALCULATOR BY HB',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/hbbots/hb-agecalculator',  
  author='HB',
  author_email='amalmohan902@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='rootcalculaor', 
  packages=find_packages(),
  install_requires=[''] 
)
