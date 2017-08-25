Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_ and this project adheres to `Semantic Versioning`_.

.. _Keep a Changelog: http://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: http://semver.org/spec/v2.0.0.html

Unreleased
----------

``1.15.0a``

Changed
^^^^^^^

- Compatibility now Python 2.7, 3.3, 3.4, 3.5, 3.6
- Defaulted to solid cell borders, so that table behavior remains consistent in the current version of Jupyter.

  - Jupyter 4.3.0 now defaults to invisible cell borders, though I am not sure in which version the change was first made
- Adopted semantic versioning

  - Planned next release will be ``1.15.0``

- Moved source into ``ipy_table`` module directory
- Moved history from README.rst to CHANGELOG.rst

Added
^^^^^
- Tests (using `py.test`)

  - Test vector generator notebook: ``ipy_table-MakeTestVectors.ipynb``
  - Test vector failure visualization notebook: ``ipy_table-VerifyTestVectors.ipynb``
  - numpy is required for testing, but not for general ipy_table installation/use

1.14 - 2017-Aug-24
------------------

- Fix email format in setup.py

1.13 - 2013-Dec-31
------------------

- Fix Unicode bug.  Unicode can now be used in cell contents. 
- Example added to ipy_table-Test.ipynb. Thanks JoshRosen for the find!

1.12 - 2013-Jan-6
-----------------

- Adopt the standard IPython display protocol.  Instead of returning an Ipython.core.display.HTML object, add the _repr_html_() method to the IpyTable class.
- Remove the get_table_html() method (no longer necessary; the table HTML can now be obtained by calling _repr_html_() explicitly).
- Remove the render() method from IpyTable (no longer necessary).
- Remove the get_table_html() function (no longer necessary; can call render()._repr_html() in interactive mode).

1.11 - 2012-Dec-30
------------------

- Initial GitHub release