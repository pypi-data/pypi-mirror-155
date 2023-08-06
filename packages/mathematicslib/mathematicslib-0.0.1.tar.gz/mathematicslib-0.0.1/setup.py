from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mathematicslib',
  version='0.0.1',
  description='A module for math',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Gustavo Kayser',
  author_email='sentick00@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='math', 
  packages=find_packages(),
  install_requires=[''] 
)