from unittest import TestCase

from ginger.libmt94x.transfer_failed_codes import InvalidCodeError
from ginger.libmt94x.transfer_failed_codes import TransferFailed
from ginger.libmt94x.transfer_failed_codes import TransferFailedMisc
from ginger.libmt94x.transfer_failed_codes import TransferFailedSEPA


class TransferFailedTests(TestCase):
    def setUp(self):
        self.sepa = TransferFailedSEPA.get_instance()
        self.misc = TransferFailedMisc.get_instance()
        self.any = TransferFailed.get_instance()

    # SEPA codes tests

    def test_sepa_code_ok(self):
        reason = self.sepa.resolve_code('AC01')
        self.assertEquals(reason, 'Rekeningnummer incorrect')

        rv = self.sepa.code_is_valid('AC01')
        self.assertEquals(rv, True)

    def test_sepa_code_invalid(self):
        # This code belongs to the Misc category
        with self.assertRaises(InvalidCodeError):
            self.sepa.resolve_code('AC03')

        rv = self.sepa.code_is_valid('AC03')
        self.assertEquals(rv, False)

    # Misc codes tests

    def test_misc_code_ok(self):
        reason = self.misc.resolve_code('AC03')
        self.assertEquals(reason, 'Ongeldig rekeningnummer crediteur')

        rv = self.misc.code_is_valid('AC03')
        self.assertEquals(rv, True)

    def test_misc_code_invalid(self):
        # This code belongs to the SEPA category
        with self.assertRaises(InvalidCodeError):
            self.misc.resolve_code('AC01')

        rv = self.misc.code_is_valid('AC01')
        self.assertEquals(rv, False)

    # Any/All codes tests

    def test_any_sepa_code_ok(self):
        # Can resolve a SEPA code
        reason = self.any.resolve_code('AC01')
        self.assertEquals(reason, 'Rekeningnummer incorrect')

        rv = self.any.code_is_valid('AC01')
        self.assertEquals(rv, True)

    def test_any_misc_code_ok(self):
        # Can resolve a Misc code
        reason = self.any.resolve_code('AC03')
        self.assertEquals(reason, 'Ongeldig rekeningnummer crediteur')

        rv = self.any.code_is_valid('AC03')
        self.assertEquals(rv, True)

    def test_any_code_invalid(self):
        # This code is not defined for either SEPA nor Misc
        with self.assertRaises(InvalidCodeError):
            self.any.resolve_code('AC00')

        rv = self.any.code_is_valid('AC00')
        self.assertEquals(rv, False)
