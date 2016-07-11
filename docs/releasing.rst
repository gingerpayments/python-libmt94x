===================================
Checklist for making a PyPI release
===================================

Housekeeping steps:

1. Bump the ``__version__`` in ``libmt94x/__init__.py``.

#. Update ``MANIFEST.in`` in case any files were added/moved/deleted.

#. Update ``HISTORY.rst`` with the new release.

#. Update ``setup.py`` with any new dependencies.

#. Update ``README.rst`` with any new information if relevant.

Before releasing first do a clean sdist build::

    $ python setup.py sdist

You can now open the ``dist/python-libmt94x-*.zip`` file using an application
like ``ark`` or similar to just do a basic sanity check on the contents of the
source distribution, make sure nothing is missing or included by mistake.

To actually push to PyPI (this will recreate the source distribution, so remove
it first)::

    $ python setup.py sdist upload
