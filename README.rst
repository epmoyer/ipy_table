:author: `Eric Moyer`_
:copyright: Copyright © 2012-2013 Eric Moyer <eric@lemoncrab.com>
:license: Modified BSD 

#########
ipy_table
#########


Overview
========

ipy_table is a support module for IPython Notebooks. ipy_table is an independent project and is not an official component of the IPython package.

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

At this time, ipy_table has only been tested with Python 2.7 under Linux and Windows.

ipy_table is designed to be used within an IPython Notebook.

IPython qtconsole operation is not currently officially supported.  ipy_table renders tables using HTML, and HTML tables render differently in the IPython qtconsole than in an IPython notebook for reasons which I have not yet unraveled.  Particularly, cell border rendering behaves differently.

Installation
============

1) Run 'python setup.py install'.

2) Copy the documentation notebooks (ipy_table-Introduction.ipynb and ipy_table-Reference.ipynb) to your main IPython notebook working directory (the directory where your IPython notebooks are stored).

If you don't know your IPython notebook working directory, start the IPython Notebook server, create a blank notebook, and execute the command 'pwd'.

Revision History
================
1.14
  Fix email format in setup.py

1.13
  Fix Unicode bug.  Unicode can now be used in cell contents. 
  Example added to ipy_table-Test.ipynb. Thanks JoshRosen for the find!

1.12
  Adopt the standard IPython display protocol.  Instead of returning
  an Ipython.core.display.HTML object, add the _repr_html_() method
  to the IpyTable class.

  Remove the get_table_html() method (no longer necessary; the table
  HTML can now be obtained by calling _repr_html_() explicitly).

  Remove the render() method from IpyTable (no longer necessary).

  Remove the get_table_html() function (no longer necessary; can call
  render()._repr_html() in interactive mode).

1.11
  Initial GitHub release


.. _`Eric Moyer`: mailto:eric@lemoncrab.com
.. _Introduction: http://nbviewer.ipython.org/urls/raw.github.com/epmoyer/ipy_table/master/ipy_table-Introduction.ipynb 
.. _Reference: http://nbviewer.ipython.org/urls/raw.github.com/epmoyer/ipy_table/master/ipy_table-Reference.ipynb    
