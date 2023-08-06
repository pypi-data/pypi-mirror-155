#!/usr/bin/env python3
import io
import os
import re
from setuptools import setup, find_packages


def read(fname):
    content = io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()
    content = re.sub(
        r'(?m)^\.\. toctree::\r?\n((^$|^\s.*$)\r?\n)*', '', content)
    return content


name = 'hb_account_statement_banque_postale_csv'

requires = [
    'wheel',
    'tryton',
    'trytond',
    'trytond_account_statement',
]

tests_require = ['proteus']

setup(
    name=name,
    version='0.2.0',
    description='',
    long_description=read('README.rst'),
    author='Hashbang',
    author_email='contact@hashbang.fr',
    url='https://hashbang.fr/',
    project_urls={
        "Bug Tracker": (
            'https://gitlab.com/hashbangfr/tryton-modules/'
            'hb_account_statement_banque_postale_csv/-/issues'
        ),
        "Source Code": (
            'https://gitlab.com/hashbangfr/tryton-modules/'
            'hb_account_statement_banque_postale_csv/'
        ),
    },
    keywords='tryton, banque postale',
    packages=find_packages(),
    package_data={
        'hb_account_statement_banque_postale_csv': [
            '*.xml',
            'tryton.cfg',
            'view/*.xml',
            'locale/*.po',
            '*.fodt',
            'icons/*.svg',
        ],
        'tests': [
            '*.rst',
            '*.csv',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business',
    ],
    license='GPL-3',
    python_requires='>=3.6',
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'trytond.modules': [
            f'{name}={name}',
        ],
    },
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    tests_require=tests_require,
)
