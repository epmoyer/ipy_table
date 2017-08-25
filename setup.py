# coding=utf-8

"""Table formatting package for IP[y] Notebooks

Copyright (c) 2012-2013, ipy_table Development Team.

Distributed under the terms of the Modified BSD License.

The full license is in the file COPYING.txt, distributed with this software.

This project is maintained at http://github.com/epmoyer/ipy_table
"""

from setuptools import setup, find_packages
from codecs import open
import os

def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return open(path, encoding='utf-8').read()

# This will set the version string to __version__
exec(read('ipy_table/version.py'))

setup(
    name="ipy_table",
    version=__version__,
    packages=find_packages(),

    # development metadata
    zip_safe=True,

    # metadata for upload to PyPI
    author="Eric Moyer",
    author_email="eric@lemoncrab.com",
    description="Creates richly formatted tables in a Jypyter Notebook",
    license="Modified BSD",
    keywords=['table', 'ipython', 'jupyter', 'notebook'],
    url='http://epmoyer.github.com/ipy_table/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Scientific/Engineering',
        ],
)
