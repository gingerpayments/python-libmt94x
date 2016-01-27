====================
libmt94x
====================

This library generates bank statements in MT940/MT942 format (for now we only
implement MT940, although the difference between the two is not major).


Concepts
========

A TM940 ``document`` is a file the represents a bank statement for a single
account between a *start date* and an *end date*. The document is built up of
``fields``, where a field has the format:

    :01:<item1>/<item2>/<item3>/

TM940 is a line-based format and each field begins on a new line. Here, ``01``
is the *tag* of the field, which uniquely identifies the format and content of
the field. These fields are modeled in ``fields.py``. The tag is followed by
items delimited with slashes. The items permitted for each field are defined in
the field definition, and items have a type and a maximum length. A field does
not exceed 65 characters, but may span multiple lines.  Lines are terminated
with ``\r\n``.

You can see example documents in ``ginger/libmt94x/tests/examples``.


Document structure
------------------

The document opens with things like the bank account number and the opening
balance.

The bulk of the document is the ``entries`` section, which contains all the
transactions that occurred between the two dates. Each ``entry`` is typically
composed of:

* A statement line:
    
  * Date of transaction
  * Type: Credit or Debit
  * Amount
  * SWIFT Transaction code
  * ING Transaction code

* Information to account owner:

  * Return reason (if the transfer represents a return)
  * Counter party id (account number, bic, name of the counter party)
  * Purpose code (what does the transfer concern?)
  * ...

The document is terminated with multiple closing balances and a summary line
that shows the number of transactions in the document, and totals for credit
and debit entries.

For a detailed description refer to the specification documents:

* Mijn ING Zakelijk (dubbed ``ming``): ``docs/spec-mt940-mijn-ing-zakelijk-aug-2014.pdf``
* Inside Business Payments (dubbed ``ibp``): ``docs/spec-mt94x-inside-business-payments-aug-2015.pdf``


Release versioning
==================

To make a release a git flow approach is used.

You need to:

* checkout and pull `develop`,
* checkout and pull `master`,
* execute `git flow release start x.x.x` ("x.x.x" = new version),
* apply release fixes/updates if needed,
* just before merging the release into master, in release branch execute `./bump-version.sh x.x.x` shell script and commit changes with message `chore(version): bumps versions to x.x.x`
* close release `git flow release finish x.x.x`
* push master,
* push tag created during release `git push origin x.x.x`
* push develop,
* check that deployment went well.
