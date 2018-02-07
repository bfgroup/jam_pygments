# Copyright 2018 Rene Rivera
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or http://www.boost.org/LICENSE_1_0.txt)

from setuptools import setup

setup(
    name='jam_pygments',
    description='A Jam/B2 build description language lexer for Pygments.',
    version='0.1',
    url='https://github.com/bfgroup/jam_pygments',
    author='Rene Rivera',
    author_email='grafikrobot@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing',
        'Topic :: Utilities',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
    ],
    keywords='pygments highlight jam b2 build boost',
    install_requires=[
        'Pygments >= 2'
    ],
    package_data={'jam_pygments': []},
    license='BSL 1.0',
    packages=['jam_pygments'],

    entry_points={
          'pygments.lexers': ['JamLexer = jam_pygments:JamLexer' ]
    },
)
