#!/usr/bin/env python3

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Matthew Burke",
    author_email='mperoburke@gmail.com',
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
    description="API wrapper library for the song history of abc radio channels",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='abc_radio_wrapper',
    name='abc_radio_wrapper',
    packages=find_packages(include=['abc_radio_wrapper', 'abc_radio_wrapper.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/matthewburke1995/abc_radio_wrapper',
    version='0.1.0',
    zip_safe=False,
)
