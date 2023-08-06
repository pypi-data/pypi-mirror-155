#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('DOC/README.rst') as readme_file:
    readme = readme_file.read()

with open('DOC/HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

with open('requirements.txt') as f:
    for line in f.readlines():
        req = line.strip()
        if not req or req.startswith('#') or '://' in req:
            continue
        requirements.append(req)

test_requirements = ['pytest>=3', ]

setup(
    author="caishengxiang",
    author_email='wancheng3833@163.com',
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
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    install_requires=requirements,
    # long_description=readme,
    include_package_data=True,
    keywords='caishengxiang',
    name='caishengxiang',
    packages=find_packages(include=['caishengxiang', 'caishengxiang.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/caishengxiang',
    version='0.1.0',
    zip_safe=False,
)
