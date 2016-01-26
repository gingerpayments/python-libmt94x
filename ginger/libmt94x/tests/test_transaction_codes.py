from unittest import TestCase

from ginger.libmt94x.transaction_codes import InvalidTransactionCodeError
from ginger.libmt94x.transaction_codes import TransactionCodes


class TransactionCodesTests(TestCase):
    def setUp(self):
        self.codes = TransactionCodes.get_instance()

    def test_code_ok(self):
        desc = self.codes.resolve_code('BNK')
        self.assertEquals(desc, 'Securities Related Item - Bank fees')

        rv = self.codes.code_is_valid('BNK')
        self.assertEquals(rv, True)

    def test_code_invalid(self):
        with self.assertRaises(InvalidTransactionCodeError):
            self.codes.resolve_code('A00')

        rv = self.codes.code_is_valid('A00')
        self.assertEquals(rv, False)
