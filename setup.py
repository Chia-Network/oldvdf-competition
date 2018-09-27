#!/usr/bin/env python

from setuptools import setup

from inkfish.version import version

setup(
    name="inkfish",
    version=version,
    packages=[
        "inkfish",
    ],
    author="Chia Network, Inc.",
    entry_points={
        'console_scripts':
            [
                'pot = inkfish.cmds:pot',
            ]
        },
    author_email="kiss@chia.net",
    url="https://github.com/Chia-Network",
    license="https://opensource.org/licenses/Apache-2.0",
    description="Verifiable delay function (proof of time) developed by Chia" +
                "Networks.",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Security :: Cryptography',
    ],)
