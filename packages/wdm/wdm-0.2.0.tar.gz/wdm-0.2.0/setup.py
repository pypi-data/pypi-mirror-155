#!/usr/bin/env python

"""The setup script."""
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open(os.path.join(here, "wdm", "version.py")) as version_file:
    exec(version_file.read())

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Heegoo Han",
    author_email='hghan9@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="webOS device manager",
    entry_points={
        'console_scripts': [
            'wdm=wdm.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wdm',
    name='wdm',
    packages=find_packages(include=['wdm', 'wdm.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/webosose-emulator/wdm',
    version=__version__,
    zip_safe=False,
)
