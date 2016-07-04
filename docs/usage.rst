=====
Usage
=====


Creating MT940 documents
========================

``libmt94x`` implements two ING-defined dialects of MT940:

* Mijn ING Zakelijk (dubbed ``ming``)

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
=====================

* For more details on the API, compatibility see docs/design.rst.

* For example MT940 documents see tests/examples/.

* For fully fleshed code examples see the tests in
  tests/test_writer_doc_XXX.py.
