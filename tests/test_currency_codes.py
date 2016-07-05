from unittest import TestCase

from libmt94x.currency_codes import CurrencyCodes
from libmt94x.currency_codes import InvalidCurrencyCodeError


class CurrencyCodesTests(TestCase):
    def setUp(self):
        self.codes = CurrencyCodes.get_instance()

    def test_code_ok(self):
        desc = self.codes.resolve_code('EUR')
        self.assertEquals(desc, 'Euro')

        rv = self.codes.code_is_valid('EUR')
        self.assertEquals(rv, True)

    def test_code_invalid(self):
        with self.assertRaises(InvalidCurrencyCodeError):
            self.codes.resolve_code('E!R')

        rv = self.codes.code_is_valid('E!R')
        self.assertEquals(rv, False)
