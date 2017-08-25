:author: `Eric Moyer`_
:copyright: Copyright © 2012-2017 Eric Moyer <eric@lemoncrab.com>
:license: Modified BSD 

#########
ipy_table
#########

|Build Status| |Coverage| |PyPIVersion| |Tag|

Overview
========

``ipy_table`` is a support module for Jupyter Notebooks. ipy_table is an independent project and is not an official component of the Jupyter package.

The home page for ``ipy_table`` is http://epmoyer.github.com/ipy_table/

``ipy_table`` is maintained at http://github.com/epmoyer/ipy_table

IPython is maintained at http://github.com/ipython, and documentation is available from http://ipython.org/

Jupyter is maintained at https://github.com/jupyter, and documentation is available at http://jupyter.org/

Documentation
=============

Documentation is provided by the documentation notebooks supplied with this package::

    notebooks/ipy_table-Introduction.ipynb
    notebooks/ipy_table-Reference.ipynb

The documentation notebooks can be viewed online with nbviewer at Introduction_ and Reference_.

Dependencies and Supported Python Versions
==========================================

``ipy_table`` works with Python 2.7, 3.3, 3.4, 3.5, and 3.6

``ipy_table`` is designed to be used within a Jupyter Notebook.

IPython qtconsole operation is not currently officially supported.  ``ipy_table`` renders tables using HTML, and HTML tables render differently in the IPython qtconsole than in a Jupyter notebook for reasons which I have not yet unraveled.  Particularly, cell border rendering behaves differently.

Installation
============

1) Run: ``pip install ipy_table``

2) Copy the documentation notebooks (``notebooks/ipy_table-Introduction.ipynb`` and ``notebooks/ipy_table-Reference.ipynb``) to your main Jupyter notebook working directory (the directory where your Jupyter notebooks are stored).

If you don't know your Jupyter notebook working directory, start the Jupyter Notebook server, create a blank notebook, and execute the command 'pwd'.

Testing
=======

To execute the tests, run ``py.test`` from the project root directory
NumPy (``numpy``) is a dependency for running the tests, but is not a dependency for installing / using ``ipy_table``

Contributors
============

Ordered by date of first contribution

- `Eric Moyer <https://github.com/epmoyer>`_ aka ``epmoyer``
- `Matthias Bussonnier <https://github.com/Carreau>`_ aka ``Carreau``
- `Josh Rosen <https://github.com/JoshRosen>`_ aka ``JoshRosen``
- `Dominic R. May <https://github.com/Mause>`_ aka ``Mause``
- `Francisco J Lopez-Pellicer <https://github.com/fjlopez>`_ aka ``fjlopez``
- `jhykes <https://githu b.com/jhykes>`_
- `Jack Lamberti <https://githu b.com/jamlamberti>`_ aka ``jamlamberti``


.. _`Eric Moyer`: mailto:eric@lemoncrab.com
.. _Introduction: http://nbviewer.ipython.org/urls/raw.github.com/epmoyer/ipy_table/master/notebooks/ipy_table-Introduction.ipynb 
.. _Reference: http://nbviewer.ipython.org/urls/raw.github.com/epmoyer/ipy_table/master/notebooks/ipy_table-Reference.ipynb
.. |Build Status| image:: https://img.shields.io/travis/epmoyer/ipy_table.svg?style=flat
   :target: https://travis-ci.org/epmoyer/ipy_table
.. |Coverage| image:: https://img.shields.io/coveralls/epmoyer/ipy_table.svg?style=flat
   :target: https://coveralls.io/github/epmoyer/ipy_table?branch=master
.. |PyPIVersion| image:: https://img.shields.io/pypi/v/ipy_table.svg?style=flat
   :target: https://pypi.python.org/pypi/ipy_table/
.. |Tag| image:: https://img.shields.io/github/tag/epmoyer/ipy_table.svg?style=flat
   :target: https://github.com/epmoyer/ipy_table/tags