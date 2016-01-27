from datetime import datetime
from decimal import Decimal
from unittest import TestCase

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
from ginger.libmt94x.info_acct_owner_subfields import PurposeCode
from ginger.libmt94x.info_acct_owner_subfields import RemittanceInformation
from ginger.libmt94x.remittance_info import UnstructuredRemittanceInfo
from ginger.libmt94x.serializer import Tm94xSerializer
from ginger.libmt94x.writer import Tm94xWriter


class Tm94xWriterTests(TestCase):
    def setUp(self):
        self.serializer = Tm94xSerializer()
        self.writer = Tm94xWriter(self.serializer)


    def test_account_identification(self):
        ai = AccountIdentification('NL69INGB0123456789', 'EUR')
        bytes = self.writer.write_account_identification(ai)
        self.assertEquals(bytes, b':25:NL69INGB0123456789EUR\r\n')

    def test_closing_available_balance(self):
        ob = ClosingAvailableBalance(
            ClosingAvailableBalance.TYPE_CREDIT,
            datetime(2014, 2, 20),
            'EUR',
            Decimal('564.35'),
        )
        bytes = self.writer.write_closing_available_balance(ob)
        self.assertEquals(bytes, b':64:C140220EUR564,35\r\n')

    def test_closing_balance(self):
        ob = ClosingBalance(
            ClosingBalance.TYPE_CREDIT,
            datetime(2014, 2, 20),
            'EUR',
            Decimal('564.35'),
        )
        bytes = self.writer.write_closing_balance(ob)
        self.assertEquals(bytes, b':62F:C140220EUR564,35\r\n')

    def test_forward_available_balance(self):
        ob = ForwardAvailableBalance(
            ForwardAvailableBalance.TYPE_CREDIT,
            datetime(2014, 2, 24),
            'EUR',
            Decimal('564.35'),
        )
        bytes = self.writer.write_forward_available_balance(ob)
        self.assertEquals(bytes, b':65:C140224EUR564,35\r\n')

    def test_information_to_account_owner_ming(self):
        info = InformationToAccountOwner(
            code_words=[
                EndToEndReference('500411584454'),
                MandateReference('1.15791632'),
                CreditorID('NL93ZZZ332656790051'),
                CounterPartyID(
                    account_number='NL12COBA0733959555',
                    bic='COBANL2XXXX',
                    name='T-Mobile Netherlands BV',
                ),
                RemittanceInformation(
                    remittance_info=UnstructuredRemittanceInfo('Factuurnummer 901258406560'),
                ),
                PurposeCode('OTHR'),
            ],
        )
        bytes = self.writer.write_information_to_account_owner_ming(info)
        expected = (
            b':86:/EREF/500411584454//MARF/1.15791632//CSID/NL93ZZZ332656790051\r\n'
            b'//CNTP/NL12COBA0733959555/COBANL2XXXX/T-Mobile Netherlands BV///R\r\n'
            b'EMI/USTD//Factuurnummer 901258406560//PURP/OTHR/\r\n'
        )
        self.assertEquals(bytes, expected)

    def test_information_to_account_owner_totals_ibp(self):
        info = InformationToAccountOwnerTotals(
            4,
            4,
            Decimal('134.46'),
            Decimal('36.58'),
        )
        bytes = self.writer.write_information_to_account_owner_totals_ibp(info)
        self.assertEquals(bytes, b':86:D4C4D134,46C36,58\r\n')

    def test_information_to_account_owner_totals_ming(self):
        info = InformationToAccountOwnerTotals(
            4,
            4,
            Decimal('134.46'),
            Decimal('36.58'),
        )
        bytes = self.writer.write_information_to_account_owner_totals_ming(info)
        self.assertEquals(bytes, b':86:/SUM/4/4/134,46/36,58/\r\n')

    def test_opening_balance(self):
        ob = OpeningBalance(
            OpeningBalance.TYPE_CREDIT,
            datetime(2014, 2, 19),
            'EUR',
            Decimal('662.23'),
        )
        bytes = self.writer.write_opening_balance(ob)
        self.assertEquals(bytes, b':60F:C140219EUR662,23\r\n')

    def test_opening_balance_zero(self):
        ob = OpeningBalance(
            OpeningBalance.TYPE_CREDIT,
            datetime(2014, 2, 19),
            'EUR',
            Decimal('0.00'),
        )
        bytes = self.writer.write_opening_balance(ob)
        self.assertEquals(bytes, b':60F:C140219EURC\r\n')

    def test_statement_line_ibp(self):
        # FIXME: Supply realistic data
        ob = StatementLine(
            value_date=datetime(2014, 2, 20),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('1.56'),
            transaction_code='TRF',
            reference_for_account_owner='EREF',
            account_servicing_institutions_reference='INGA00000XXXX',
            ing_transaction_code='00100',
        )
        bytes = self.writer.write_statement_line_ibp(ob)
        self.assertEquals(
            bytes,
            b':61:140220C1,56NTRFEREFINGA00000XXXX/TRCD/00100/\r\n'
        )

    def test_statement_line_ming(self):
        ob = StatementLine(
            value_date=datetime(2014, 2, 20),
            book_date=datetime(2000, 2, 20),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('1.56'),
            transaction_code='TRF',
            reference_for_account_owner='EREF',
            transaction_reference='00000000001005',
            ing_transaction_code='00100',
        )
        bytes = self.writer.write_statement_line_ming(ob)
        expected = (
            b':61:1402200220C1,56NTRFEREF//00000000001005\r\n'
            b'/TRCD/00100/\r\n'
        )
        self.assertEquals(bytes, expected)

    def test_statement_number(self):
        sn = StatementNumber('00000')
        bytes = self.writer.write_statement_number(sn)
        self.assertEquals(bytes, b':28C:00000\r\n')

    def test_transaction_reference_number_ibp(self):
        trn = TransactionReferenceNumber()
        bytes = self.writer.write_transaction_reference_number_ibp(trn)
        self.assertEquals(bytes, b':20:ING\r\n')

    def test_transaction_reference_number_ming(self):
        trn = TransactionReferenceNumber('P140220000000001')
        bytes = self.writer.write_transaction_reference_number_ming(trn)
        self.assertEquals(bytes, b':20:P140220000000001\r\n')
