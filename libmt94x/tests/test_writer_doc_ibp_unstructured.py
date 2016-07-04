from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from unittest import TestCase
import os

from libmt94x.document import Mt940Document
from libmt94x.fields import AccountIdentification
from libmt94x.fields import ClosingAvailableBalance
from libmt94x.fields import ClosingBalance
from libmt94x.fields import ExportInformation
from libmt94x.fields import ForwardAvailableBalance
from libmt94x.fields import ImportInformation
from libmt94x.fields import InformationToAccountOwner
from libmt94x.fields import InformationToAccountOwnerTotals
from libmt94x.fields import OpeningBalance
from libmt94x.fields import StatementLine
from libmt94x.fields import StatementNumber
from libmt94x.fields import TransactionReferenceNumber
from libmt94x.serializer import Mt94xSerializer
from libmt94x.writer import Mt94xWriter


class Mt94xWriterIBPUnstructuredTests(TestCase):
    def setUp(self):
        self.serializer = Mt94xSerializer()
        self.writer = Mt94xWriter(self.serializer)


    def test_doc_ibp_unstructured_spec(self):
        # Create the entries first

        line1 = StatementLine(
            value_date=datetime(2013, 11, 4),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('0.02'),
            transaction_code='NOV',
            reference_for_account_owner='EREF',
        )
        info1 = InformationToAccountOwner(
            free_form_text=(
                b'NL20INGB0002222222 INGBNL2A Creditor Name 01 E2ENA01014ULT2410201'
                b'3T1100xxxx1xxxx UstrNA01014ULT24102013T1100xxxx1xxx ULTCREDNM07 S'
                b'ECT01014 ULTDEBTNM04 SECT01014'
            ),
        )

        line2 = StatementLine(
            value_date=datetime(2013, 11, 4),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('0.04'),
            transaction_code='NOV',
            reference_for_account_owner='EREF',
        )
        info2 = InformationToAccountOwner(
            free_form_text=(
                b'NL20INGB0002222222 INGBNL2A Creditor Name 11 E2ENA0101b4ULT241020'
                b'13T1100xxxx1xxx 2062542165530231 ULTCREDNM08 SECT01014 ULTDEBTNM0'
                b'4 SECT01014'
            ),
        )

        line3 = StatementLine(
            value_date=datetime(2013, 11, 4),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('0.09'),
            transaction_code='NOV',
            reference_for_account_owner='EREF',
        )
        info3 = InformationToAccountOwner(
            free_form_text=(
                b'NL12INGB0003333333 INGBNL2A Creditor Name 09 E2ENA01014c4ULT24102'
                b'013T1100xxxx1xx RF35567890123456789012345 ULTCREDNM09 SECT01014 U'
                b'LTDEBTNM04 SECT01014'
            ),
        )

        line4 = StatementLine(
            value_date=datetime(2013, 11, 4),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('0.02'),
            transaction_code='NOV',
            reference_for_account_owner='EREF',
        )
        info4 = InformationToAccountOwner(
            free_form_text=(
                b'AC04 NL20INGB0002222222 INGBNL2A Creditor Name 01 E2ENA01014ULT24'
                b'102013T1100xxxx1xxxx UstrNA01014ULT24102013T1100xxxx1xxx ULTCREDN'
                b'M07 SECT01014 ULTDEBTNM04 SECT01014'
            )
        )

        line5 = StatementLine(
            value_date=datetime(2013, 11, 4),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('0.04'),
            transaction_code='NOV',
            reference_for_account_owner='EREF',
        )
        info5 = InformationToAccountOwner(
            free_form_text=(
                b'MS03 NL20INGB0002222222 INGBNL2A Creditor Name 11 E2ENA0101b4ULT2'
                b'4102013T1100xxxx1xxx 2062542165530231 ULTCREDNM08 SECT01014 ULTDE'
                b'BTNM04 SECT01014'
            ),
        )

        # Wire the entries up
        entries = OrderedDict([
            (line1, [info1]),
            (line2, [info2]),
            (line3, [info3]),
            (line4, [info4]),
            (line5, [info5]),
        ])

        doc = Mt940Document(
            export_info=ExportInformation(
                export_address='INGBNL2AXXXX',
                export_number='00001',
            ),
            import_info=ImportInformation(
                import_address='INGBNL2AXXXX',
                import_number='00001',
            ),
            transaction_reference_number=TransactionReferenceNumber(),
            account_identification=AccountIdentification(
                iban='NL20INGB0001234567',
                iso_currency_code='EUR'
            ),
            statement_number=StatementNumber('1'),
            opening_balance=OpeningBalance(
                OpeningBalance.TYPE_CREDIT,
                datetime(2013, 11, 4),
                'EUR',
                Decimal('0.0'),
            ),
            entries=entries,
            closing_balance=ClosingBalance(
                ClosingBalance.TYPE_DEBIT,
                datetime(2013, 11, 4),
                'EUR',
                Decimal('0.09'),
            ),
            closing_available_balance=ClosingAvailableBalance(
                ClosingAvailableBalance.TYPE_DEBIT,
                datetime(2013, 11, 4),
                'EUR',
                Decimal('0.09'),
            ),
            forward_available_balances=[
                ForwardAvailableBalance(
                    ForwardAvailableBalance.TYPE_DEBIT,
                    datetime(2013, 11, 5),
                    'EUR',
                    Decimal('0.09'),
                ),
                ForwardAvailableBalance(
                    ForwardAvailableBalance.TYPE_DEBIT,
                    datetime(2013, 11, 6),
                    'EUR',
                    Decimal('0.09'),
                ),
            ],
            info_to_acct_owner_totals=InformationToAccountOwnerTotals(
                num_debit=3,
                num_credit=2,
                amount_debit=Decimal('0.15'),
                amount_credit=Decimal('0.06'),
            ),
        )

        bytes = self.writer.write_document_ibp(doc)

        # Load spec file
        fp_spec = os.path.join(
            os.path.dirname(__file__), 'examples', 'ibp-unstructured-ing-provided-example.txt')
        with open(fp_spec, 'rb+') as f:
            expected = f.read()

        self.assertEquals(bytes, expected)
