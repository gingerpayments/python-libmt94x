======================
libmt94x compatibility
======================

This file documents the compatibility testing we have done for our
implementation, and known variations in the wild.



MT940 MING dialect
==================

Examples we have:

1. ``ming-from-spec.txt``. This is the document included in the spec ``docs/spec-mt940-mijn-ing-zakelijk-aug-2014.pdf``
2. ``ming-ing-provided-example-single-message.txt`` is an example document provided by ING (one message per file)
3. ``ming-ing-provided-example-multiple-messages.txt`` is an example document provided by ING (multiple messages per file)


Variations between (1) and (2)/(3)
----------------------------------

The export/import fields are inline and there is an additional field with tag ``3``::

    {1:F01INGBNL2ABXXX0000000000}{2:I940INGBNL2AXXXN}{3:{108:B12345678S000001}}{4:

The info to account owner summary field contains items ``NAME`` and ``BIC`` not found
in the spec::

    :86:/NAME/ING BANK N.V.//BIC/INGBNL2A// SUM/1/0/15,00/0,/


Importing in accounting software
--------------------------------

========== =============== ==============
Input file e-boekhouden.nl exactonline.nl
========== =============== ==============
    (1)        OK*              OK*
    (2)        OK*              OK*
    (3)        OK*              OK*
========== =============== ==============

* Tested on Jan 27, 2016



MT940 IBP dialect
=================

Examples we have:

1. ``ibp-unstructured-ing-provided-example.txt`` is an example unstructured document provided by ING
2. ``ibp-structured-ing-provided-example.txt`` is an example structured document provided by ING
3. ``ibp-structured-ing-provided-example-edited.txt`` is an edited version (2)


Variations between (2) and (3)
------------------------------

The provided example contains unstructured REMI fields::

    /REMI///EV1551551REP180112T1544/

This is a pre-autumn 2014 format and has been edited to the current::

    /REMI/USTD//EV1551551REP180112T1544/


Importing in accounting software
--------------------------------

========== =============== ==============
Input file e-boekhouden.nl exactonline.nl
========== =============== ==============
    (1)        OK*              OK*
    (2)        OK+              OK+
    (3)        OK+              OK+
========== =============== ==============

* Tested on Jan 29, 2016
+ Tested on Feb 1, 2016
