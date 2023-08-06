from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='bstmapcbe',
  version='0.0.1',
  description='A Package used for finding the routes for important places in Coimbatore,India By Arjun K PSG ICE',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Arjun K',
  author_email='arjunkrishnarajv@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='map',
  packages=find_packages(),
  install_requires=[''] 
)