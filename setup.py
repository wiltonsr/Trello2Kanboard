# -*- coding: utf-8 -*-

import io
import re

from setuptools import setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('trello2kanboard/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='Trello2Kanboard',
    version=version,
    license='BSD',
    url='https://github.com/wiltonsr/Trello2Kanboard',
    author='Wilton Rodrigues',
    author_email='wiltonsr94@gmail.com',
    description='Simple Python Package for Importing Trello Projects from JSON Files Using the Kanboard API.',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['trello2kanboard', 'trello2kanboard.commands'],
    include_package_data=True,
    install_requires=[
        'click',
        'kanboard',
        'python-dateutil'
    ],
    entry_points='''
        [console_scripts]
        trello2kanboard=trello2kanboard.cli:cli
    ''',
)
