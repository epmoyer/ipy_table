:author: `Eric Moyer`_
:copyright: Copyright © 2012 Eric Moyer <eric@lemoncrab.com>
:license: Modified BSD 

#########
ipy_table
#########


Overview
========

ipy_table is a support module for . ipy_table is an independent project and is not an official component of the IPython package.

ipy_table is maintained at http://github.com/epmoyer/ipy_table

ipython is maintained at http://github.com/ipython, and documentation is available from http://ipython.org/

Documentation
=============

Documentation is provided by the documentation notebooks supplied with this package::

    ipy_table-Introduction.ipynb
    ipy_table-Reference.ipynb
    
PDF versions have also been provided for easy reference.

Dependencies and Supported Python Versions
==========================================

At this time, ipy_table has only been tested with Python 2.7 under Linux and Windows.

ipy_table is designed to be used within an IPython Notebook.

IPython qtconsole operation is not currently officially supported.  ipy_table renders tables using HTML, and HTML tables render differently in the IPython qtconsole than in an IPython notebook for reasons which I have not yet unraveled.  Particularly, cell border rendering behaves differently.

Installation
============

1) Run 'python setup.py install'.

2) Copy the documentation notebooks (ipy_table-Introduction.ipynb and ipy_table-Reference.ipynb) to your main IPython notebook working directory (the directory where your IPython notebooks are stored).

If you don't know your IPython notebook working directory, start the IPython Notebook server, create a blank notebook, and execute the command 'pwd'.

.. _`Eric Moyer`: mailto:eric@lemoncrab.com
