#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['pandas>=1.1.0', 'numpy>=1.19.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Martin Luther Bironga",
    email="tutorialcreation81@gmail.com",
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="A package that helps interact with lidar data from satelites",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='scripts',
    name='geolidar',
    packages=find_packages(include=['scripts', 'scripts.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/10xac/PythonPackageStructure',
    version='0.0.2',
    zip_safe=False,
)
