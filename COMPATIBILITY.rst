======================
libmt94x compatibility
======================


MT940 MING dialect
==================

Examples we have:

1. ``ming-from-spec.txt``. This is the document included in the spec ``docs/spec-mt940-mijn-ing-zakelijk-aug-2014.pdf``
2. ``ing-provided-example-single-message.txt`` is an example document provided by ING (one message per file)
3. ``ing-provided-example-multiple-messages.txt`` is an example document provided by ING (multiple messages per file)


Variations between (1) and (2)/(3)
----------------------------------

The export/import fields are inline and there is an additional field with tag ``3``::

    {1:F01INGBNL2ABXXX0000000000}{2:I940INGBNL2AXXXN}{3:{108:B12345678S000001}}{4:

The info to account owner summary field contains items ``NAME`` and ``BIC`` not found
in the spec::

    :86:/NAME/ING BANK N.V.//BIC/INGBNL2A// SUM/1/0/15,00/0,/


Testing against accounting software
-----------------------------------

========== =============== ============
Input file e-boekhouden.nl exact online
========== =============== ============
    (1)        OK
    (2)        OK
    (3)        OK
========== =============== ============
