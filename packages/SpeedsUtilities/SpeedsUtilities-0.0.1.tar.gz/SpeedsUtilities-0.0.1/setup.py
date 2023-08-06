from setuptools import setup, find_packages

classifiers = ['Development Status :: 5 - Production/Stable',
'Intended Audience :: Developers',
'Operating System :: Microsoft :: Windows :: Windows 10',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3.6'
]

setup(
name='SpeedsUtilities',
version='0.0.1',
description='A few utlitites',
long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
url='',
author='Pavel Martinek',
author_email='pavlicekcz292@gmail.com',
license='MIT',
classifiers=classifiers,
keywords='button',
packages=find_packages(),
install_requires=['pygame']
)