from unittest import TestCase

from ginger.libmt94x.info_account_owner_subfields import CounterPartyID
from ginger.libmt94x.info_account_owner_subfields import CreditorID
from ginger.libmt94x.info_account_owner_subfields import EndToEndReference
from ginger.libmt94x.info_account_owner_subfields import MandateReference
from ginger.libmt94x.info_account_owner_subfields import PaymentInformationID
from ginger.libmt94x.info_account_owner_subfields import PurposeCode
from ginger.libmt94x.info_account_owner_subfields import RemittanceInformation
from ginger.libmt94x.info_account_owner_subfields import ReturnReason
from ginger.libmt94x.info_account_owner_subfields import UltimateCreditor
from ginger.libmt94x.info_account_owner_subfields import UltimateDebtor
from ginger.libmt94x.remittance_info import DutchStructuredRemittanceInfo
from ginger.libmt94x.remittance_info import IsoStructuredRemittanceInfo
from ginger.libmt94x.remittance_info import UnstructuredRemittanceInfo
from ginger.libmt94x.serializer import Tm94xSerializer
from ginger.libmt94x.writer import Tm94xWriter


class Tm94xWriterInfoToAcctOwnerSubfieldsTests(TestCase):
    def setUp(self):
        self.serializer = Tm94xSerializer()
        self.writer = Tm94xWriter(self.serializer)

    # Counter party tests

    def test_counter_party_id(self):
        cntp = CounterPartyID(
            account_number='NL12COBA0733959555',
            bic='COBANL2XXXX',
            name='T-Mobile Netherlands BV',
            city='AMSTERDAM',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, cntp)
        bytes = self.serializer.finish()

        self.assertEquals(
            bytes,
            b'/CNTP/NL12COBA0733959555/COBANL2XXXX/T-Mobile Netherlands BV/AMSTERDAM/',
        )

    def test_counter_party_id_missing_account_number(self):
        cntp = CounterPartyID(
            bic='COBANL2XXXX',
            name='T-Mobile Netherlands BV',
            city='AMSTERDAM',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, cntp)
        bytes = self.serializer.finish()

        self.assertEquals(
            bytes,
            b'/CNTP//COBANL2XXXX/T-Mobile Netherlands BV/AMSTERDAM/',
        )

    def test_counter_party_id_missing_bic(self):
        cntp = CounterPartyID(
            account_number='NL12COBA0733959555',
            name='T-Mobile Netherlands BV',
            city='AMSTERDAM',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, cntp)
        bytes = self.serializer.finish()

        self.assertEquals(
            bytes,
            b'/CNTP/NL12COBA0733959555//T-Mobile Netherlands BV/AMSTERDAM/',
        )

    def test_counter_party_id_missing_name(self):
        cntp = CounterPartyID(
            account_number='NL12COBA0733959555',
            bic='COBANL2XXXX',
            city='AMSTERDAM',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, cntp)
        bytes = self.serializer.finish()

        self.assertEquals(
            bytes,
            b'/CNTP/NL12COBA0733959555/COBANL2XXXX//AMSTERDAM/',
        )

    def test_counter_party_id_missing_city(self):
        cntp = CounterPartyID(
            account_number='NL12COBA0733959555',
            bic='COBANL2XXXX',
            name='T-Mobile Netherlands BV',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, cntp)
        bytes = self.serializer.finish()

        self.assertEquals(
            bytes,
            b'/CNTP/NL12COBA0733959555/COBANL2XXXX/T-Mobile Netherlands BV//',
        )

    # Creditor ID tests

    def test_creditor_id(self):
        csid = CreditorID('NL93ZZZ332656790051')

        self.serializer.start()
        self.writer._write_code_word(self.serializer, csid)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/CSID/NL93ZZZ332656790051/')

    # EndToEndReference tests

    def test_end_to_end_reference(self):
        eref = EndToEndReference('500411584454')

        self.serializer.start()
        self.writer._write_code_word(self.serializer, eref)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/EREF/500411584454/')

    # MandateReference tests

    def test_mandate_reference(self):
        marf = MandateReference('1.15791632')

        self.serializer.start()
        self.writer._write_code_word(self.serializer, marf)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/MARF/1.15791632/')

    # PaymentInformationID tests

    def test_payment_information_id(self):
        pref = PaymentInformationID('PMTINFID1401038')

        self.serializer.start()
        self.writer._write_code_word(self.serializer, pref)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/PREF/PMTINFID1401038/')

    # PurposeCode tests

    def test_purpose_code(self):
        purp = PurposeCode('OTHR')

        self.serializer.start()
        self.writer._write_code_word(self.serializer, purp)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/PURP/OTHR/')

    # RemittanceInformation tests

    def test_remittance_info_unstructured(self):
        remi = RemittanceInformation(
            remittance_info=UnstructuredRemittanceInfo(
                'TERUGGAAF  NR. 819301243U5         MOTO'
                'RRYTUIGENB.15 (BOERJSBEHEER)'
            )
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, remi)
        bytes = self.serializer.finish()

        # No line breaks expected since this is just a single subfield
        expected = (
            b'/REMI/USTD//TERUGGAAF  NR. 819301243U5         MOTO'
            b'RRYTUIGENB.15 (BOERJSBEHEER)/'
        )
        self.assertEquals(bytes, expected)

    def test_remittance_info_dutch_structured(self):
        remi = RemittanceInformation(
            remittance_info=DutchStructuredRemittanceInfo('6390338414964113')
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, remi)
        bytes = self.serializer.finish()

        # No line breaks expected since this is just a single subfield
        expected = b'/REMI/STRD/CUR/6390338414964113/'
        self.assertEquals(bytes, expected)

    def test_remittance_info_iso_structured(self):
        remi = RemittanceInformation(
            remittance_info=IsoStructuredRemittanceInfo('6390338414964113')
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, remi)
        bytes = self.serializer.finish()

        # No line breaks expected since this is just a single subfield
        expected = b'/REMI/STRD/ISO/6390338414964113/'
        self.assertEquals(bytes, expected)

    # ReturnReason tests

    def test_return_reason(self):
        rtrn = ReturnReason('MD04')

        self.serializer.start()
        self.writer._write_code_word(self.serializer, rtrn)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/RTRN/MD04/')

    # UltimateCreditor tests

    def test_ultimate_creditor(self):
        ultc = UltimateCreditor(
            name='T-Mobile Netherlands BV',
            id='16013724426777',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, ultc)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/ULTC/T-Mobile Netherlands BV/16013724426777/')

    def test_ultimate_creditor_missing_name(self):
        ultc = UltimateCreditor(
            id='16013724426777',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, ultc)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/ULTC//16013724426777/')

    def test_ultimate_creditor_missing_id(self):
        ultc = UltimateCreditor(
            name='T-Mobile Netherlands BV',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, ultc)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/ULTC/T-Mobile Netherlands BV//')

    # UltimateDebtor tests

    def test_ultimate_debtor(self):
        ultd = UltimateDebtor(
            name='T-Mobile Netherlands BV',
            id='16013724426777',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, ultd)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/ULTD/T-Mobile Netherlands BV/16013724426777/')

    def test_ultimate_debtor_missing_name(self):
        ultd = UltimateDebtor(
            id='16013724426777',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, ultd)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/ULTD//16013724426777/')

    def test_ultimate_debtor_missing_id(self):
        ultd = UltimateDebtor(
            name='T-Mobile Netherlands BV',
        )

        self.serializer.start()
        self.writer._write_code_word(self.serializer, ultd)
        bytes = self.serializer.finish()

        self.assertEquals(bytes, b'/ULTD/T-Mobile Netherlands BV//')
