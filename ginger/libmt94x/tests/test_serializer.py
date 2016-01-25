from unittest import TestCase

from ginger.libmt94x.serializer import Tm94xSerializer


class Tm94xSerializerTests(TestCase):
    def setUp(self):
        self.ser = Tm94xSerializer()

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

    def test_number_charset_too_long(self):
        # Exceeds field length
        with self.assertRaises(ValueError):
            self.ser.serialize_value(self.ser.type_num, 3, b'ab3a')

    # Numeric tests

    def test_number_charset_value_range(self):
        # All digits are accepted (and leading zero is preserved)
        value_range = b'0123456789'
        val = self.ser.serialize_value(self.ser.type_num, len(value_range), value_range)
        self.assertEquals(val, value_range)

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
