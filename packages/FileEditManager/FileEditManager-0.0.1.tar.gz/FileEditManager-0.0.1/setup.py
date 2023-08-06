from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='FileEditManager',
  version='0.0.1',
  description='A very basic package',
  url='',  
  author='me',
  author_email='opkoskos450@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='File', 
  packages=find_packages(),
  install_requires=[''] 
)