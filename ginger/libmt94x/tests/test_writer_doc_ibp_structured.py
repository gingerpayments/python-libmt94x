from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from unittest import TestCase
import os

from ginger.libmt94x.document import Mt940Document
from ginger.libmt94x.fields import AccountIdentification
from ginger.libmt94x.fields import ClosingAvailableBalance
from ginger.libmt94x.fields import ClosingBalance
from ginger.libmt94x.fields import ExportInformation
from ginger.libmt94x.fields import ForwardAvailableBalance
from ginger.libmt94x.fields import ImportInformation
from ginger.libmt94x.fields import InformationToAccountOwner
from ginger.libmt94x.fields import InformationToAccountOwnerTotals
from ginger.libmt94x.fields import OpeningBalance
from ginger.libmt94x.fields import StatementLine
from ginger.libmt94x.fields import StatementNumber
from ginger.libmt94x.fields import TransactionReferenceNumber
from ginger.libmt94x.info_acct_owner_subfields import BeneficiaryParty
from ginger.libmt94x.info_acct_owner_subfields import BusinessPurpose
from ginger.libmt94x.info_acct_owner_subfields import CreditorID
from ginger.libmt94x.info_acct_owner_subfields import EndToEndReference
from ginger.libmt94x.info_acct_owner_subfields import MandateReference
from ginger.libmt94x.info_acct_owner_subfields import PaymentInformationID
from ginger.libmt94x.info_acct_owner_subfields import RemittanceInformation
from ginger.libmt94x.info_acct_owner_subfields import ReturnReason
from ginger.libmt94x.remittance_info import UnstructuredRemittanceInfo
from ginger.libmt94x.serializer import Mt94xSerializer
from ginger.libmt94x.writer import Mt94xWriter


class Mt94xWriterIBPStructuredTests(TestCase):
    def setUp(self):
        self.serializer = Mt94xSerializer()
        self.writer = Mt94xWriter(self.serializer)


    def test_doc_ibp_structured_spec(self):
        # Create the entries first

        line1 = StatementLine(
            value_date=datetime(2012, 1, 30),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('1.45'),
            transaction_code='038',
            reference_for_account_owner='MARF',
        )
        info1 = InformationToAccountOwner(
            code_words=[
                ReturnReason('MS03'),
                BusinessPurpose(
                    id_code='Europese Incasso',
                    sepa_transaction_type='eenmalig',
                ),
                BeneficiaryParty(
                    account_number='NL50INGB0001234567',
                    bic='INGBNL2A',
                    name='ING Bank N.V. inzake WeB',
                ),
                CreditorID('NL32ZZZ999999991234'),
                MandateReference('EV45451'),
                EndToEndReference('EV45451REP170112T1106'),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo(
                        'EV45451REP170112T1106'
                    ),
                ),
            ],
        )

        line2 = StatementLine(
            value_date=datetime(2012, 1, 30),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('2.56'),
            transaction_code='036',
            reference_for_account_owner='EREF',
        )
        info2 = InformationToAccountOwner(
            code_words=[
                BeneficiaryParty(
                    account_number='NL38INGB0654321789',
                    bic='INGBNL2A',
                    name='ING Bank NV inzake EBW PP',
                ),
                EndToEndReference('EV1551551REP180112T1544'),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo(
                        'EV1551551REP180112T1544'
                    ),
                ),
            ],
        )

        line3 = StatementLine(
            value_date=datetime(2012, 1, 30),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('2.57'),
            transaction_code='036',
            reference_for_account_owner='PREF',
        )
        info3 = InformationToAccountOwner(
            code_words=[
                BusinessPurpose(
                    id_code='Verzamel Eurobetaling',
                ),
                PaymentInformationID('M000000002222222'),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo(
                        'TOTAAL 1 POSTEN'
                    ),
                ),
            ],
        )

        # Wire the entries up
        entries = OrderedDict([
            (line1, [info1]),
            (line2, [info2]),
            (line3, [info3]),
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
                iban='0654321789',
            ),
            statement_number=StatementNumber('21'),
            opening_balance=OpeningBalance(
                OpeningBalance.TYPE_CREDIT,
                datetime(2012, 1, 27),
                'EUR',
                Decimal('26.10'),
            ),
            entries=entries,
            closing_balance=ClosingBalance(
                ClosingBalance.TYPE_CREDIT,
                datetime(2012, 1, 30),
                'EUR',
                Decimal('19.52'),
            ),
            closing_available_balance=ClosingAvailableBalance(
                ClosingAvailableBalance.TYPE_CREDIT,
                datetime(2012, 1, 30),
                'EUR',
                Decimal('19.52'),
            ),
            forward_available_balances=[
                ForwardAvailableBalance(
                    ForwardAvailableBalance.TYPE_CREDIT,
                    datetime(2012, 1, 31),
                    'EUR',
                    Decimal('19.52'),
                ),
                ForwardAvailableBalance(
                    ForwardAvailableBalance.TYPE_CREDIT,
                    datetime(2012, 2, 1),
                    'EUR',
                    Decimal('19.52'),
                ),
            ],
            info_to_acct_owner_totals=InformationToAccountOwnerTotals(
                num_debit=3,
                num_credit=0,
                amount_debit=Decimal('6.58'),
                amount_credit=Decimal('0.00'),
            ),
        )

        bytes = self.writer.write_document_ibp(doc)

        # Load spec file
        fp_spec = os.path.join(
            os.path.dirname(__file__), 'examples', 'ibp-structured-ing-provided-example-edited.txt')
        with open(fp_spec, 'rb+') as f:
            expected = f.read()

        self.assertEquals(bytes, expected)
