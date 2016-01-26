from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from ginger.libmt94x.document import Tm94xDocument
from ginger.libmt94x.fields import AccountIdentification
from ginger.libmt94x.fields import ClosingAvailableBalance
from ginger.libmt94x.fields import ClosingBalance
from ginger.libmt94x.fields import ForwardAvailableBalance
from ginger.libmt94x.fields import InformationToAccountOwner
from ginger.libmt94x.fields import InformationToAccountOwnerTotals
from ginger.libmt94x.fields import OpeningBalance
from ginger.libmt94x.fields import StatementLine
from ginger.libmt94x.fields import StatementNumber
from ginger.libmt94x.fields import TransactionReferenceNumber
from ginger.libmt94x.info_acct_owner_subfields import CounterPartyID
from ginger.libmt94x.info_acct_owner_subfields import CreditorID
from ginger.libmt94x.info_acct_owner_subfields import EndToEndReference
from ginger.libmt94x.info_acct_owner_subfields import MandateReference
from ginger.libmt94x.info_acct_owner_subfields import PaymentInformationID
from ginger.libmt94x.info_acct_owner_subfields import PurposeCode
from ginger.libmt94x.info_acct_owner_subfields import RemittanceInformation
from ginger.libmt94x.info_acct_owner_subfields import ReturnReason
from ginger.libmt94x.remittance_info import DutchStructuredRemittanceInfo
from ginger.libmt94x.remittance_info import UnstructuredRemittanceInfo
from ginger.libmt94x.serializer import Tm94xSerializer
from ginger.libmt94x.writer import Tm94xWriter


class Tm94xWriterTests(TestCase):
    def setUp(self):
        self.serializer = Tm94xSerializer()
        self.writer = Tm94xWriter(self.serializer)


    def test_doc_ming_spec(self):
        # Create the entries first

        line1 = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('1.56'),
            transaction_code='TRF',
            reference_for_account_owner='EREF',
            transaction_reference='00000000001005',
            ing_transaction_code='00100',
        )
        info1 = InformationToAccountOwner(
            code_words=[
                EndToEndReference('EV12341REP1231456T1234'),
                CounterPartyID(
                    account_number='NL32INGB0000012345',
                    bic='INGBNL2A',
                    name='ING BANK NV INZAKE WEB',
                ),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo('EV10001REP1000000T1000'),
                ),
            ],
        )

        line2 = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('1.57'),
            transaction_code='TRF',
            reference_for_account_owner='PREF',
            transaction_reference='00000000001006',
            ing_transaction_code='00200',
        )
        info2 = InformationToAccountOwner(
            code_words=[
                PaymentInformationID('M000000003333333'),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo('TOTAAL 1 VZ'),
                ),
            ],
        )

        line3 = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('1.57'),
            transaction_code='RTI',
            reference_for_account_owner='EREF',
            transaction_reference='00000000001007',
            ing_transaction_code='00190',
        )
        info3 = InformationToAccountOwner(
            code_words=[
                ReturnReason('MS03'),
                EndToEndReference('20120123456789'),
                CounterPartyID(
                    account_number='NL32INGB0000012345',
                    bic='INGBNL2A',
                    name='J.Janssen',
                ),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo(
                        'Factuurnr 123456 Klantnr 00123'
                    ),
                ),
            ],
        )

        line4 = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('1.14'),
            transaction_code='DDT',
            reference_for_account_owner='EREF',
            transaction_reference='00000000001009',
            ing_transaction_code='01016',
        )
        info4 = InformationToAccountOwner(
            code_words=[
                EndToEndReference('EV123REP123412T1234'),
                MandateReference('MND-EV01'),
                CreditorID('NL32ZZZ999999991234'),
                CounterPartyID(
                    account_number='NL32INGB0000012345',
                    bic='INGBNL2A',
                    name='ING Bank N.V. inzake WeB',
                ),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo(
                        'EV123REP123412T1234',
                    ),
                ),
            ],
        )

        line5 = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('1.45'),
            transaction_code='DDT',
            reference_for_account_owner='PREF',
            transaction_reference='00000000001008',
            ing_transaction_code='01000',
        )
        info5 = InformationToAccountOwner(
            code_words=[
                PaymentInformationID('M000000001111111'),
                CreditorID('NL32ZZZ999999991234'),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo(
                        'TOTAAL      1 POSTEN',
                    ),
                ),
            ],
        )

        line6 = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('12.75'),
            transaction_code='RTI',
            reference_for_account_owner='EREF',
            transaction_reference='00000000001010',
            ing_transaction_code='01315',
        )
        info6 = InformationToAccountOwner(
            code_words=[
                ReturnReason('MS03'),
                EndToEndReference('20120501P0123478'),
                MandateReference('MND-120123'),
                CreditorID('NL32ZZZ999999991234'),
                CounterPartyID(
                    account_number='NL32INGB0000012345',
                    bic='INGBNL2A',
                    name='J.Janssen',
                ),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo(
                        'CONTRIBUTIE FEB 2014',
                    ),
                ),
            ],
        )

        line7 = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('32.00'),
            transaction_code='TRF',
            reference_for_account_owner='9001123412341234',
            transaction_reference='00000000001011',
            ing_transaction_code='00108',
        )
        info7 = InformationToAccountOwner(
            code_words=[
                EndToEndReference('15814016000676480'),
                CounterPartyID(
                    account_number='NL32INGB0000012345',
                    bic='INGBNL2A',
                    name='J.Janssen',
                ),
                RemittanceInformation(
                    remittance_info=DutchStructuredRemittanceInfo(
                        '9001123412341234',
                    ),
                ),
            ],
        )

        line8 = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('119.00'),
            transaction_code='TRF',
            reference_for_account_owner='1070123412341234',
            transaction_reference='00000000001012',
            ing_transaction_code='00108',
        )
        info8 = InformationToAccountOwner(
            code_words=[
                EndToEndReference('15614016000384600'),
                CounterPartyID(
                    account_number='NL32INGB0000012345',
                    bic='INGBNL2A',
                    name='INGBANK NV',
                ),
                RemittanceInformation(
                    remittance_info=DutchStructuredRemittanceInfo(
                        '1070123412341234',
                    ),
                ),
            ],
        )

        # Wire the entries up
        entries = OrderedDict([
            (line1, [info1]),
            (line2, [info2]),
            (line3, [info3]),
            (line4, [info4]),
            (line5, [info5]),
            (line6, [info6]),
            (line7, [info7]),
            (line8, [info8]),
        ])

        doc = Tm94xDocument(
            transaction_reference_number=TransactionReferenceNumber('P140220000000001'),
            account_identification=AccountIdentification('NL69INGB0123456789', 'EUR'),
            statement_number=StatementNumber('00000'),
            opening_balance=OpeningBalance(
                OpeningBalance.TYPE_CREDIT,
                datetime(2014, 2, 19),
                'EUR',
                Decimal('662.23'),
            ),
            entries=entries,
            closing_balance=ClosingBalance(
                ClosingBalance.TYPE_CREDIT,
                datetime(2014, 2, 20),
                'EUR',
                Decimal('564.35'),
            ),
            closing_available_balance=ClosingAvailableBalance(
                ClosingAvailableBalance.TYPE_CREDIT,
                datetime(2014, 2, 20),
                'EUR',
                Decimal('564.35'),
            ),
            forward_available_balances=[
                ForwardAvailableBalance(
                    ForwardAvailableBalance.TYPE_CREDIT,
                    datetime(2014, 2, 21),
                    'EUR',
                    Decimal('564.35'),
                ),
                ForwardAvailableBalance(
                    ForwardAvailableBalance.TYPE_CREDIT,
                    datetime(2014, 2, 24),
                    'EUR',
                    Decimal('564.35'),
                ),
            ],
            info_to_acct_owner_totals=InformationToAccountOwnerTotals(
                4,
                4,
                Decimal('134.46'),
                Decimal('36.58'),
            ),
        )

        bytes = self.writer.write_document_ming(doc)
        print bytes
