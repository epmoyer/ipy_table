:author: `Eric Moyer`_
:copyright: Copyright © 2012-2017 Eric Moyer <eric@lemoncrab.com>
:license: Modified BSD 

#########
ipy_table
#########

|Build Status| |Coverage| |Version|

Overview
========

ipy_table is a support module for Jupyter Notebooks. ipy_table is an independent project and is not an official component of the Jupyter package.

The home page for ipy_table is http://epmoyer.github.com/ipy_table/

ipy_table is maintained at http://github.com/epmoyer/ipy_table

ipython is maintained at http://github.com/ipython, and documentation is available from http://ipython.org/

Documentation
=============

Documentation is provided by the documentation notebooks supplied with this package::

    ipy_table-Introduction.ipynb
    ipy_table-Reference.ipynb

The documentation notebooks can be viewed online with nbviewer at Introduction_ and Reference_.

Dependencies and Supported Python Versions
==========================================

At this time, ipy_table has only been tested with Python 2.7 under Linux and Windows.  Test coverage and Travis integration have been added to support development of Python 3 compatibility.

ipy_table is designed to be used within a Jupyter Notebook.

IPython qtconsole operation is not currently officially supported.  ipy_table renders tables using HTML, and HTML tables render differently in the IPython qtconsole than in a Jupyter notebook for reasons which I have not yet unraveled.  Particularly, cell border rendering behaves differently.

Installation
============

1) Run ``python setup.py install``.

2) Copy the documentation notebooks (ipy_table-Introduction.ipynb and ipy_table-Reference.ipynb) to your main Jupyter notebook working directory (the directory where your Jupyter notebooks are stored).

If you don't know your Jupyter notebook working directory, start the Jupyter Notebook server, create a blank notebook, and execute the command 'pwd'.

Testing
=======

To execute the tests, run ``py.test`` from the project root directory

.. _`Eric Moyer`: mailto:eric@lemoncrab.com
.. _Introduction: http://nbviewer.ipython.org/urls/raw.github.com/epmoyer/ipy_table/master/ipy_table-Introduction.ipynb 
.. _Reference: http://nbviewer.ipython.org/urls/raw.github.com/epmoyer/ipy_table/master/ipy_table-Reference.ipynb
.. |Build Status| image:: http://img.shields.io/travis/epmoyer/ipy_table.svg?style=flat-square
   :target: https://travis-ci.org/epmoyer/ipy_table
.. |Coverage| image:: http://img.shields.io/coveralls/epmoyer/ipy_table.svg?style=flat-square
   :target: https://coveralls.io/r/epmoyer/ipy_table
.. |Version| image:: http://img.shields.io/pypi/v/ipy_table.svg?style=flat-square
   :target: https://pypi.python.org/pypi/ipy_table/