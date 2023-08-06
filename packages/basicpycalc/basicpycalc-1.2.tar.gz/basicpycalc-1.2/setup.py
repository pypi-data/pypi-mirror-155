from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='basicpycalc',
  version='1.2',
  description='This is a clock extension which creates a basic clock using a few modules. If you have any questions, mail me at - ananyo.bhattacharya2010@gmail.com',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read() + '\n\n' + open('LICENSE.txt').read(),
  url='',  
  author='Ananyo Bhattacharya',
  author_email='ananyo.bhattacharya2010@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[] 
)