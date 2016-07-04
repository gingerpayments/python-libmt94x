=========================
Design and implementation
=========================

This library generates bank account statements in MT940/MT942 format (for now we only
implement MT940, although the difference between the two is not major).

Note that this library is written based mostly on ING specifications, so it is
(heavily) slanted towards ING usage of the MT940 format.



Concepts
========

A MT940 ``document`` is a file the represents a bank statement for a single
account between a *start date* and an *end date* (the dates themselves are not
stored in the document). The document is built up of ``fields``, where a field
has the format::

    :01:<item1>/<item2>/<item3>/

MT940 is a line-based format and each field begins on a new line. Here, ``01``
is the *tag* of the field, which uniquely identifies the format and content of
the field. These fields are modeled in ``fields.py``. The tag is followed by
items delimited with slashes. The items permitted for each field are defined in
the field definition, and items have a type and a maximum length. A field does
not exceed 65 characters, but may span multiple lines.  Lines are terminated
with ``\r\n``.



Document structure
==================

The document has a prolog::

    {1:F01INGBNL2ABXXX0000000000}   # export information
    {2:I940INGBNL2AXXXN}            # import information
    {4:                             # start of message information

The document opens with things like the bank account number and the opening
balance::

    :20:P140104000009999            # transaction reference number
    :25:NL20INGB0001234567EUR       # account identification
    :28C:3                          # statement number
    :60F:C140102EUR1000,00          # opening balance

The bulk of the document is the ``entries`` section, which contains all the
transactions that occurred between the two dates. Each ``entry`` is typically
composed of::

    :61:1401030103D12,00NTRFEREF//00000000000003
    /TRCD/01025/
    :86:/EREF/E2E420140103318//MARF/MNDTID012545488665//CSID/NL99ZZZ99999
    9999999//CNTP/NL08INGB0000001234/INGBNL2A/ING Testrekening/AMSTER
    DAM//REMI/USTD//INGB20140103UstrdRemiInf454655GHF/

* A statement line (tag ``61``):

  * Value date of transaction (here ``140103``)
  * Book date of transaction (here ``0103``)
  * Type: Credit or Debit (``C`` or ``D``)
  * Amount (here ``12,00``)
  * SWIFT Transaction code (four characters, begins with ``N``, here ``NTRF``)
  * Reference for account owner (here ``EREF``)
  * Transaction reference (here ``00000000000003``)
  * ING constant keyword (``TRCD``)
  * ING Transaction code (five digits, here ``01025``)

* Information to account owner (tag ``86``):

  * Return reason (if the transfer represents a return)
  * Counter party id ``CNTP`` (account number, bic, name of the counter party)
  * Purpose code (what does the transfer concern?)
  * ...

The document is terminated with multiple closing balances and a summary line
that shows the number of transactions in the document, and totals for credit
and debit entries::

    :62F:C160115EUR2149,31              # closing balance
    :64:C160115EUR2149,31               # closing available balance
    :65:C160116EUR2149,31               # forward available balance
    :65:C160117EUR2149,31               # forward available balance
    :86:/SUM/6/2/8448,01/1414,00/       # 6 debit, 2 credit, debit amount, credit amount
    -}                                  # message terminator

Note that the fact that the tag ``86`` appears both in an entry *and* in the
summary part of the document is not an error. It is actually two different
fields with the same tag.

For a detailed description refer to the specification documents:

* Mijn ING Zakelijk: ``specs/spec-mt940-mijn-ing-zakelijk-aug-2014.pdf``
* Inside Business Payments: ``specs/spec-mt94x-inside-business-payments-aug-2015.pdf``

You can find example documents in ``tests/examples``.


Dialects
--------

The story is complicated slightly by the fact that we have to handle two
dialects of MT940:

* Mijn ING Zakelijk (dubbed ``ming``)
* Inside Business Payments (dubbed ``ibp``)

Each is described in the spec, but not all example documents adhere exactly
to the spec, so there is some uncertainty involved.



Implementation assumptions
==========================

* We only implement MT940, not MT942. MT940 is used to generate "final" bank
  statements, whereas MT942 is used to obtain tentative bank statements - these
  are much less useful to us.
* We do not implement the Consolidated Statement, because this is an aggregate
  statement for all the transactions, whereas we want to export all the
  transactions one by one.
* The IBP spec mentions two formats: pre-autumn 2014 (legacy) and post-autumn
  2014 (current). We do not care about the legacy format.
* The library does not perform any semantic support, it only implements a data
  format. This means totals for transactions are not checked, nor inferred.
  Whatever data you provide will be written - the library just enforces that
  the output format is correct.



Implementation
==============


Components
----------

Serializer
~~~~~~~~~~

The SWIFT data format (cited in the specs) defines two data types:

* characters (with a restricted character set)
* numbers (digits)

The purpose of the serializer is to enforce that all bytes written to the
document respect these definitions, and that no field or subfield exceeds
its maximum size. *All bytes written to the document pass through the 
serializer* - you can also think of it as a filter.

The serializer API exposes methods to serialize single values, but it also
exposes a chaining API that allows writing fields in a style very similar to
the way it's defined in the spec::

        field = (self.serializer
                 .start()
                 .chars(4, ':65:')            # 4-char tag
                 .chars(1, 'C')               # 1-char credit/debit type
                 .num(6, '140221')            # 6-digit date YYMMDD
                 .chars(3, 'EUR')             # 3-char currency
                 .chars(15, '564,35')         # 15-char amount
                 .newline()                   # \r\n
                 .finish()
        )

Fields
~~~~~~

Fields are modeled as classes derived from the abstract ``Field`` base, with
each of their data items as attributes.  Fields validate their input data where
possible (dates must be ``datetime`` objects, amount values must be ``Decimal``
objects, transaction codes are checked against a list of valid codes).

Note that fields do not contain information about the sizes of their data,
this is handled by the ``Writer``.

Document
~~~~~~~~

The class ``Mt940Document`` models an MT940 document and enforces which fields
must be provided.

Writer
~~~~~~

The writer knows how to write fields and documents. It does this through the
``Serializer``. In the case of variations in the output format (``ming`` vs
``ibp``), the writer is the ultimate authority on what must be written.


Tests
-----

Unit tests are provided for each component and whenever we model a new field or
subfield (or a new dialect), tests need to be added.

Tests also provide the most accurate documentation on how the APIs are intended
to be used.



Compatibility
=============

Here we document the compatibility testing we have done for our implementation,
and known variations in the wild.



MT940 MING dialect
------------------

Examples we have:

1. ``ming-from-spec.txt``. This is the document included in the spec ``specs/spec-mt940-mijn-ing-zakelijk-aug-2014.pdf``
2. ``ming-ing-provided-example-single-message.txt`` is an example document provided by ING (one message per file)
3. ``ming-ing-provided-example-multiple-messages.txt`` is an example document provided by ING (multiple messages per file)

We implement (1).


Variations between (1) and (2)/(3)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The export/import fields are inline and there is an additional field with tag ``3``::

    {1:F01INGBNL2ABXXX0000000000}{2:I940INGBNL2AXXXN}{3:{108:B12345678S000001}}{4:

The info to account owner summary field contains items ``NAME`` and ``BIC`` not found
in the spec::

    :86:/NAME/ING BANK N.V.//BIC/INGBNL2A// SUM/1/0/15,00/0,/


Importing in accounting software
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

========== =============== ==============
Input file e-boekhouden.nl exactonline.nl
========== =============== ==============
    (1)        OK^              OK^
    (2)        OK^              OK^
    (3)        OK^              OK^
========== =============== ==============

* ^ Tested on Jan 27, 2016



MT940 IBP dialect
-----------------

Examples we have:

1. ``ibp-unstructured-ing-provided-example.txt`` is an example unstructured document provided by ING
2. ``ibp-structured-ing-provided-example.txt`` is an example structured document provided by ING
3. ``ibp-structured-ing-provided-example-edited.txt`` is an edited version of (2)

We implement (1) and (3).


Variations between (2) and (3)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The provided example contains unstructured REMI fields::

    /REMI///EV1551551REP180112T1544/

This is a pre-autumn 2014 format and has been edited to the current::

    /REMI/USTD//EV1551551REP180112T1544/


Importing in accounting software
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

========== =============== ==============
Input file e-boekhouden.nl exactonline.nl
========== =============== ==============
    (1)        OK^              OK^
    (2)        OK%              OK%
    (3)        OK%              OK%
========== =============== ==============

* ^ Tested on Jan 29, 2016
* % Tested on Feb 1, 2016
