from setuptools import setup

setup(
    name='pumuckl',
    version='0.1.0',
    py_modules=['pumuckl'],
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
)
