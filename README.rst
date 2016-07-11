========
libmt94x
========


.. image:: https://api.travis-ci.org/gingerpayments/python-libmt94x.png?branch=develop
    :target: https://travis-ci.org/gingerpayments/python-libmt94x

.. image:: https://scrutinizer-ci.com/g/gingerpayments/python-libmt94x/badges/coverage.png?b=develop
    :target: https://scrutinizer-ci.com/g/gingerpayments/python-libmt94x/


MT940/MT942 is a text based data file format used in bank account statements
(commonly used by banks in the Netherlands). A bank account statement contains
your account balance as well as a listing of all the transactions between a
given start date and end date.

This library provides an API to define and serialize MT940/MT942 documents in
Python. It does not provide a parser.




Installation
============

TODO: pip install instructions




Usage
=====


Creating MT940 documents
------------------------

``libmt94x`` implements two ING-defined dialects of MT940:

* Mijn ING Zakelijk (dubbed ``ming``),

* Inside Business Payments (dubbed ``ibp``).

No matter which dialect your are using you first need to construct an
``MT940Document`` and then use the appropriate method to write it out
to the target dialect::


    from libmt94x.document import Mt940Document
    from libmt94x.fields import AccountIdentification
    # ...snip...
    from libmt94x.fields import TransactionReferenceNumber
    from libmt94x.serializer import Mt94xSerializer
    from libmt94x.writer import Mt94xWriter


    serializer = Mt94xSerializer()
    writer = Mt94xWriter(serializer)

    doc = Mt940Document(
        transaction_reference_number=TransactionReferenceNumber('P140220000000001'),
        account_identification=AccountIdentification('NL69INGB0123456789', 'EUR'),
        # ...snip...
    )

    # to write using the ``ming`` dialect
    bytestring = writer.write_document_ming(doc)

    # to write using the ``ibp`` dialect
    bytestring = writer.write_document_ibp(doc)


How to find more info
---------------------

* For more details on the API and compatibility issues see docs/design.rst.

* For example MT940 documents see tests/examples/.

* For fully fledged code examples see the tests in
  tests/test_writer_doc_XXX.py.




Developing on libmt94x
======================


Running tests
-------------

It is recommended that you use a virtualenv when working on libmt94x. To run
tests you will first need to install the development dependencies, which
include ``tox``::

    $ pip install -r dev-requirements.txt

Now run the tests using tox (this will invoke py.test inside the tox-managed
virtual test environment)::

    $ tox

This will run tests, collect test coverage and run the style checker
``flake8``. For a more lightweight test run you can run pytest directly::

    $ py.test


Contributing
------------

Please see CONTRIBUTING.rst for guidelines on how to contribute to libmt94x.
