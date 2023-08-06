=====
flats
=====

Minimal library that enables flattening of nested instances of container types.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/flats.svg
   :target: https://badge.fury.io/py/flats
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/flats/badge/?version=latest
   :target: https://flats.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/lapets/flats/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/lapets/flats/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/lapets/flats/badge.svg?branch=main
   :target: https://coveralls.io/github/lapets/flats?branch=main
   :alt: Coveralls test coverage summary.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/flats>`__::

    python -m pip install flats

The library can be imported in the usual ways::

    import flats
    from flats import flats

Examples
^^^^^^^^

.. |Iterable| replace:: ``Iterable``
.. _Iterable: https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable

.. |GeneratorType| replace:: ``GeneratorType``
.. _GeneratorType: https://docs.python.org/3/library/types.html#types.GeneratorType

This library provides a function that can flatten any instance of a container type that is the root of a tree of nested instances of container types, returning as an iterable the sequence of all objects or values (that are not of a container type) encountered during an in-order traversal. Any instance of the |Iterable|_ class or of the |GeneratorType|_ is considered to be an instance of a container type by this library::

    >>> from flats import flats
    >>> list(flats([[1, 2, 3], [4, 5, 6, 7]]))
    [1, 2, 3, 4, 5, 6, 7]

The nested instances need not be of the same type::

    >>> tuple(flats([{1}, {2}, {3}, frozenset({4}), iter([5, 6, 7])]))
    (1, 2, 3, 4, 5, 6, 7)
    >>> list(flats(['abc', 'xyz']))
    ['a', 'b', 'c', 'x', 'y', 'z']
    >>> list(flats([range(3), range(3)]))
    [0, 1, 2, 0, 1, 2]

It is also possible to limit the depth to which nested instances of a container type are recursively traversed during the flattening process (leaving unmodified the nesting of any instances that are found at a greater depth)::

    >>> list(flats([[[1, 2], 3], [4, 5, 6, 7]], depth=1))
    [[1, 2], 3, 4, 5, 6, 7]
    >>> list(flats([[[1, 2], 3], [4, 5, 6, 7]], depth=2))
    [1, 2, 3, 4, 5, 6, 7]
    >>> list(flats([[[1, [2]], 3], [4, [[[5]]], 6, 7]], depth=float('inf')))
    [1, 2, 3, 4, 5, 6, 7]

Development
-----------
All installation and development dependencies are managed using `setuptools <https://pypi.org/project/setuptools>`__ and are fully specified in ``setup.py``. The ``extras_require`` parameter is used to `specify optional requirements <https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#optional-dependencies>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__::

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__::

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see ``setup.cfg`` for configuration details)::

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__::

    python flats/flats.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org>`__::

    python -m pip install .[lint]
    python -m pylint flats

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/lapets/flats>`__ for this library.

Versioning
^^^^^^^^^^
Beginning with version 0.1.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/flats>`__ by a package maintainer. First, install the dependencies required for packaging and publishing::

    python -m pip install .[publish]

Remove any old build/distribution files. Then, package the source into a distribution archive using the `wheel <https://pypi.org/project/wheel>`__ package::

    rm -rf dist *.egg-info
    python setup.py sdist bdist_wheel

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__ using the `twine <https://pypi.org/project/twine>`__ package::

    python -m twine upload dist/*
