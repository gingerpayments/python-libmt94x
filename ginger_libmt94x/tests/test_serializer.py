from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from ginger_libmt94x.serializer import Mt94xSerializer


class Mt94xSerializerTests(TestCase):
    def setUp(self):
        self.ser = Mt94xSerializer()

    # Character tests

    def test_char_charset_lowercase(self):
        lowercase = b'abcdefghijklmnopqrstuvwxyz'
        val = self.ser.serialize_value(self.ser.type_char, len(lowercase), lowercase)
        self.assertEquals(val, lowercase)

    def test_char_charset_uppercase(self):
        uppercase = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        val = self.ser.serialize_value(self.ser.type_char, len(uppercase), uppercase)
        self.assertEquals(val, uppercase)

    def test_char_charset_digits(self):
        digits = b'0123456789'
        val = self.ser.serialize_value(self.ser.type_char, len(digits), digits)
        self.assertEquals(val, digits)

    def test_char_charset_special_chars(self):
        specials = b"/-?().,+'{}: "
        val = self.ser.serialize_value(self.ser.type_char, len(specials), specials)
        self.assertEquals(val, specials)

    def test_char_charset_outside_range(self):
        # Try with some low bytes
        with self.assertRaises(ValueError):
            self.ser.serialize_value(self.ser.type_char, 3, b'\x00\x01')

    def test_char_charset_too_long(self):
        # Exceeds field length
        with self.assertRaises(ValueError):
            self.ser.serialize_value(self.ser.type_char, 3, b'ab3a')

    # Numeric tests

    def test_number_charset_value_range(self):
        # All digits are accepted (and leading zero is preserved)
        value_range = b'0123456789'
        val = self.ser.serialize_value(self.ser.type_num, len(value_range), value_range)
        self.assertEquals(val, value_range)

    def test_number_charset_leading_zeroes(self):
        value = b'123'
        val = self.ser.serialize_value(self.ser.type_num, 6, value, leading_zeroes=6)
        self.assertEquals(val, '000123')

    def test_number_charset_outside_range(self):
        # Decimal point not allowed
        with self.assertRaises(ValueError):
            self.ser.serialize_value(self.ser.type_num, 10, b'123.10')

    def test_number_charset_too_long(self):
        # Exceeds field length
        with self.assertRaises(ValueError):
            self.ser.serialize_value(self.ser.type_num, 3, b'1234')

    def test_number_charset_wrong_type(self):
        # Try to write as characters
        with self.assertRaises(ValueError):
            self.ser.serialize_value(self.ser.type_num, 3, b'abc')

    # Newline tests

    def test_newline(self):
        val = self.ser.serialize_newline()
        self.assertEquals(val, b'\r\n')

    # Amount tests

    def test_amount_ok(self):
        val = self.ser.serialize_amount(15, 'EUR', Decimal('101.45'))
        self.assertEquals(val, b'101,45')

    def test_amount_too_long(self):
        with self.assertRaises(ValueError):
            self.ser.serialize_amount(4, 'EUR', Decimal('101.45'))

    def test_amount_wrong_type(self):
        with self.assertRaises(ValueError):
            self.ser.serialize_amount(15, 'EUR', 12.32)

    def test_amount_negative(self):
        with self.assertRaises(ValueError):
            self.ser.serialize_amount(15, 'EUR', Decimal('-101.45'))

    # Date tests

    def test_date_ok(self):
        val = self.ser.serialize_date('%y%m%d', datetime(2014, 2, 3))
        self.assertEquals(val, b'140203')

    def test_date_wrong_type(self):
        with self.assertRaises(ValueError):
            self.ser.serialize_date('%y%m%d', '140203')

    # Chaining tests

    def test_chain_api(self):
        val = (self.ser
               .start()
               .chars(4, ':65:')
               .chars(1, 'C')
               .num(6, '140221')
               .chars(3, 'EUR')
               .chars(15, '564,35')
               .newline()
               .finish()
        )
        self.assertEquals(val, b':65:C140221EUR564,35\r\n')

    def test_chars_noslash(self):
        self.ser.start()
        with self.assertRaises(ValueError):
            self.ser.chars_noslash(45, 'A/B testing is cool')
