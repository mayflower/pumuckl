from setuptools import setup
import os

long_description = 'Check a Puppetfile for modules with newer versions'
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
    name='pumuckl',
    version='0.2.0',
    description='Check a Puppetfile for modules with newer versions',
    long_description=long_description,
    author ='Robin Gloster',
    author_email ='robin.gloster@mayflower.de',
    url='https://github.com/Mayflower/pumuckl',
    packages=['pumuckl'],
    license='GPL v3',
    install_requires=[
        'Click',
        'pyparsing',
        'asyncio',
        'aiohttp',
        'semantic_version',
    ],
    entry_points='''
        [console_scripts]
        pumuckl=pumuckl:cli
    ''',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
    ]
)
