from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from ginger_libmt94x.fields import AccountIdentification
from ginger_libmt94x.fields import ClosingAvailableBalance
from ginger_libmt94x.fields import ClosingBalance
from ginger_libmt94x.fields import ExportInformation
from ginger_libmt94x.fields import ForwardAvailableBalance
from ginger_libmt94x.fields import InformationToAccountOwner
from ginger_libmt94x.fields import InformationToAccountOwnerTotals
from ginger_libmt94x.fields import ImportInformation
from ginger_libmt94x.fields import OpeningBalance
from ginger_libmt94x.fields import StatementLine
from ginger_libmt94x.fields import StatementNumber
from ginger_libmt94x.fields import TransactionReferenceNumber
from ginger_libmt94x.info_acct_owner_subfields import CounterPartyID
from ginger_libmt94x.info_acct_owner_subfields import CreditorID
from ginger_libmt94x.info_acct_owner_subfields import EndToEndReference
from ginger_libmt94x.info_acct_owner_subfields import MandateReference
from ginger_libmt94x.info_acct_owner_subfields import PurposeCode
from ginger_libmt94x.info_acct_owner_subfields import RemittanceInformation
from ginger_libmt94x.statement_line_subfields import OriginalAmountOfTransaction
from ginger_libmt94x.remittance_info import UnstructuredRemittanceInfo
from ginger_libmt94x.serializer import Mt94xSerializer
from ginger_libmt94x.writer import Mt94xWriter


class Mt94xWriterTests(TestCase):
    def setUp(self):
        self.serializer = Mt94xSerializer()
        self.writer = Mt94xWriter(self.serializer)

    # AccountIdentification

    def test_account_identification(self):
        ai = AccountIdentification('NL69INGB0123456789', 'EUR')
        bytes = self.writer.write_account_identification(ai)
        self.assertEquals(bytes, b':25:NL69INGB0123456789EUR\r\n')

    # ClosingAvailableBalance

    def test_closing_available_balance(self):
        ob = ClosingAvailableBalance(
            ClosingAvailableBalance.TYPE_CREDIT,
            datetime(2014, 2, 20),
            'EUR',
            Decimal('564.35'),
        )
        bytes = self.writer.write_closing_available_balance(ob)
        self.assertEquals(bytes, b':64:C140220EUR564,35\r\n')

    # ClosingBalance

    def test_closing_balance(self):
        ob = ClosingBalance(
            ClosingBalance.TYPE_CREDIT,
            datetime(2014, 2, 20),
            'EUR',
            Decimal('564.35'),
        )
        bytes = self.writer.write_closing_balance(ob)
        self.assertEquals(bytes, b':62F:C140220EUR564,35\r\n')

    # ExportInformation

    def test_export_info_ibp(self):
        ei = ExportInformation(
            export_address='INGBNL2AXXXX',
            export_number='00001',
        )
        bytes = self.writer.write_export_info_ibp(ei)
        self.assertEquals(bytes, b'0000 01INGBNL2AXXXX00001\r\n')

    # ForwardAvailableBalance

    def test_forward_available_balance(self):
        ob = ForwardAvailableBalance(
            ForwardAvailableBalance.TYPE_CREDIT,
            datetime(2014, 2, 24),
            'EUR',
            Decimal('564.35'),
        )
        bytes = self.writer.write_forward_available_balance(ob)
        self.assertEquals(bytes, b':65:C140224EUR564,35\r\n')

    # InformationToAccountOwner

    def test_information_to_account_owner_ibp_both_types(self):
        # Cannot pass both code_words and free_form_text
        with self.assertRaises(ValueError):
            InformationToAccountOwner(
                code_words=[
                    EndToEndReference('500411584454'),
                ],
                free_form_text=b'a',
            )

    def test_information_to_account_owner_ibp_structured(self):
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
        bytes = self.writer.write_information_to_account_owner_ibp(info)
        expected = (
            b':86:/EREF/500411584454//MARF/1.15791632//CSID/NL93ZZZ332656790051//CN\r\n'
            b'TP/NL12COBA0733959555/COBANL2XXXX/T-Mobile Netherlands BV///REMI/\r\n'
            b'USTD//Factuurnummer 901258406560//PURP/OTHR/\r\n'
        )
        self.assertEquals(bytes, expected)

    def test_information_to_account_owner_ibp_unstructured_flattened(self):
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
        info.flatten()  # flatten the structured subfields to free form text

        bytes = self.writer.write_information_to_account_owner_ibp(info)
        expected = (
            b':86:500411584454 1.15791632 NL93ZZZ332656790051 NL12COBA0733959555 CO\r\n'
            b'BANL2XXXX T-Mobile Netherlands BV Factuurnummer 901258406560 OTHR\r\n'
        )
        self.assertEquals(bytes, expected)

    def test_information_to_account_owner_ibp_unstructured_free_form(self):
        info = InformationToAccountOwner(
            free_form_text=(
                b'NL20INGB0002222222 INGBNL2A Creditor Name 11 E2ENA0101b4ULT241020'
                b'13T1100xxxx1xxx 2062542165530231 ULTCREDNM08 SECT01014 ULTDEBTNM0'
                b'4 SECT01014'
            )
        )
        bytes = self.writer.write_information_to_account_owner_ibp(info)
        expected = (
            b':86:NL20INGB0002222222 INGBNL2A Creditor Name 11 E2ENA0101b4ULT241020\r\n'
            b'13T1100xxxx1xxx 2062542165530231 ULTCREDNM08 SECT01014 ULTDEBTNM0\r\n'
            b'4 SECT01014\r\n'
        )
        self.assertEquals(bytes, expected)

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

    # InformationToAccountOwnerTotals

    def test_information_to_account_owner_totals_ibp(self):
        info = InformationToAccountOwnerTotals(
            4,
            4,
            Decimal('134.46'),
            Decimal('36.58'),
        )
        bytes = self.writer.write_information_to_account_owner_totals_ibp(info)
        self.assertEquals(bytes, b':86:D000004C000004D134,46C36,58\r\n')

    def test_information_to_account_owner_totals_ming(self):
        info = InformationToAccountOwnerTotals(
            4,
            4,
            Decimal('134.46'),
            Decimal('36.58'),
        )
        bytes = self.writer.write_information_to_account_owner_totals_ming(info)
        self.assertEquals(bytes, b':86:/SUM/4/4/134,46/36,58/\r\n')

    # ImportInformation

    def test_import_info_ibp(self):
        ii = ImportInformation(
            import_address='INGBNL2AXXXX',
            import_number='00001',
        )
        bytes = self.writer.write_import_info_ibp(ii)
        self.assertEquals(bytes, b'0000 01INGBNL2AXXXX00001\r\n')

    # OpeningBalance

    def test_opening_balance(self):
        ob = OpeningBalance(
            OpeningBalance.TYPE_CREDIT,
            datetime(2014, 2, 19),
            'EUR',
            Decimal('662.23'),
        )
        bytes = self.writer.write_opening_balance(ob)
        self.assertEquals(bytes, b':60F:C140219EUR662,23\r\n')

    # NOTE: Disabled because none of the documents in the wild we have seen
    # actually follow this part of the spec
    def _test_opening_balance_zero(self):
        ob = OpeningBalance(
            OpeningBalance.TYPE_CREDIT,
            datetime(2014, 2, 19),
            'EUR',
            Decimal('0.00'),
        )
        bytes = self.writer.write_opening_balance(ob)
        self.assertEquals(bytes, b':60F:C140219EURC\r\n')

    # StatementLine

    def test_statement_line_ibp(self):
        ob = StatementLine(
            value_date=datetime(2014, 2, 20),
            type=StatementLine.TYPE_CREDIT,
            amount=Decimal('1.56'),
            transaction_code='TRF',
            reference_for_account_owner='EREF',
            account_servicing_institutions_reference='INGA00000XXXX',
            ing_transaction_code='00100',
            original_amount_of_transaction=OriginalAmountOfTransaction(
                currency='USD',
                amount=Decimal('1234.50'),
            ),
        )
        bytes = self.writer.write_statement_line_ibp(ob)
        self.assertEquals(
            bytes,
            b':61:140220C1,56NTRFEREFINGA00000XXXX/TRCD/00100//OCMT/USD1234,50/\r\n'
        )

    def test_statement_line_ibp_minimalist(self):
        ob = StatementLine(
            value_date=datetime(2013, 11, 04),
            type=StatementLine.TYPE_DEBIT,
            amount=Decimal('0.02'),
            transaction_code='036',
            reference_for_account_owner='EREF',
        )
        bytes = self.writer.write_statement_line_ibp(ob)
        self.assertEquals(
            bytes,
            b':61:131104D0,02N036EREF\r\n',
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

    # StatementNumber

    def test_statement_number(self):
        sn = StatementNumber('00000')
        bytes = self.writer.write_statement_number(sn)
        self.assertEquals(bytes, b':28C:00000\r\n')

    # TransactionReferenceNumber

    def test_transaction_reference_number_ibp(self):
        trn = TransactionReferenceNumber()
        bytes = self.writer.write_transaction_reference_number_ibp(trn)
        self.assertEquals(bytes, b':20:ING\r\n')

    def test_transaction_reference_number_ming(self):
        trn = TransactionReferenceNumber('P140220000000001')
        bytes = self.writer.write_transaction_reference_number_ming(trn)
        self.assertEquals(bytes, b':20:P140220000000001\r\n')
