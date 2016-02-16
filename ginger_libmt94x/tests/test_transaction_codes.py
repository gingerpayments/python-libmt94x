from unittest import TestCase

from ginger_libmt94x.transaction_codes import IngTransactionCodes
from ginger_libmt94x.transaction_codes import InvalidIngTransactionCodeError
from ginger_libmt94x.transaction_codes import InvalidSwiftTransactionCodeError
from ginger_libmt94x.transaction_codes import SwiftTransactionCodes


class IngTransactionCodesTests(TestCase):
    def setUp(self):
        self.codes = IngTransactionCodes.get_instance()

    def test_code_ok(self):
        desc = self.codes.resolve_code('00100')
        self.assertEquals(desc, 'SEPA Credit Transfer')

        rv = self.codes.code_is_valid('00100')
        self.assertEquals(rv, True)

    def test_code_invalid(self):
        with self.assertRaises(InvalidIngTransactionCodeError):
            self.codes.resolve_code('11000')

        rv = self.codes.code_is_valid('11000')
        self.assertEquals(rv, False)


class SwiftTransactionCodesTests(TestCase):
    def setUp(self):
        self.codes = SwiftTransactionCodes.get_instance()

    def test_code_ok(self):
        desc = self.codes.resolve_code('BNK')
        self.assertEquals(desc, 'Securities Related Item - Bank fees')

        rv = self.codes.code_is_valid('BNK')
        self.assertEquals(rv, True)

    def test_code_invalid(self):
        with self.assertRaises(InvalidSwiftTransactionCodeError):
            self.codes.resolve_code('A00')

        rv = self.codes.code_is_valid('A00')
        self.assertEquals(rv, False)
