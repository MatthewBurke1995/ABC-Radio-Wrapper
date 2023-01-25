#!/usr/bin/env python3

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "requests>=2.27.1"
]

test_requirements = [
        "mypy>=0.991",
        "mypy-extensions>=0.4.3",
        "types-requests>=2.28.11.8",
        "types-urllib3>=1.26.25.4",
        "typing_extensions>=4.4.0",
        "requests>=2.27.1",
        "black>=22.12.0",
        "flake8>==6.0.0",
        "Sphinx>=5.3.0",
        "sphinx-rtd-theme>=1.1.1"
]

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
    url='https://github.com/MatthewBurke1995/ABC-Radio-Wrapper',
    version='0.2.0',
    zip_safe=False,
)
