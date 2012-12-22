OVERVIEW
========
ipy_table is a support module for creating formatted tables in an IPython Notebook. ipy_table is an independant project and is not an official component of the IPython package.

ipy_table is availabe from http://github.com/ipy_table

ipython is availble from http://github.com/ipython, and documentation is available from http://ipython.org/

DOCUMENTATION
=============
Documentation is provided by the documentation notebooks supplied with this package:
    ipy_table-Introduction.ipynb
    ipy_table-Reference.ipynb

DEPENDENCIES AND SUPPORTED PYTHON VERSIONS
==========================================
At this time, ipy_table has only been tested with Python 2.7 under Linux and Windows.

ipy_table is designed to be used within an IPython Notebook.

IPython qtconsole operation is not currently officially supported.  ipy_table renders tables using HTML, and HTML tables render differently in the IPython qtconsole than in an IPython notebook for reasons which I have not yet unraveled.  Particularly, cell border rendering behaves differently.

INSTALLATION
============
Copy ipy_table.py and the documentation notebooks (ipy_table-Introduction.ipynb and ipy_table-Reference.ipynb) to your main IPython notebook working directory (the directory where your IPython notebooks are stored).

If you don't know your IPython notebook working directory, start the IPython Notebook server, create a blank notebook, and execute the command 'pwd'.
