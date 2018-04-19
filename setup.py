#!/usr/bin/env python
import os
from setuptools import setup, find_packages


setup(
    name='django_db_view',
    version=__import__('django_db_view').__version__,
    author='martin',
    author_email='ma.tongji@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Artistic License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Database',
    ],
    #test_suite="runtests.runtests",
    #tests_require=['mock'],
    zip_safe=False,  # because we're including media that Django needs
)

