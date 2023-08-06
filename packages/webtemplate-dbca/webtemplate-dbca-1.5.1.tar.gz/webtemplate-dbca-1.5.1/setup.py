#!/usr/bin/env python

from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

install_requires = [
    'Django>=2.2',
]
version = ('1.5.1')

setup(
    name='webtemplate-dbca',
    version=version,
    install_requires=install_requires,
    tests_require=install_requires,
    test_suite='runtests.runtests',
    packages=['webtemplate_dbca'],
    include_package_data=True,
    author='Ashley Felton',
    author_email='asi@dbca.wa.gov.au',
    maintainer='Ashley Felton',
    maintainer_email='asi@dbca.wa.gov.au',
    license='Apache License, Version 2.0',
    url='https://github.com/dbca-wa/webtemplate',
    description='Base HTML templates for DBCA Django projects',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords=['django', 'html', 'template', 'bootstrap'],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
