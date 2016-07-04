from datetime import datetime
from decimal import Decimal
import re

from libmt94x.textutil import format_amount


# NOTE: Module level binding since we want to use the name "type" in method
# signatures
builtin_type = type


class Mt94xSerializer(object):
    TYPE_CHARACTER = 1
    TYPE_NUMERIC = 2

    swift_charset_chars = (
        b"abcdefghijklmnopqrstuvwxyz"
        b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        b"0123456789"
        b"/-?().,+'{}: "
    )
    swift_charset_numbers = b"0123456789"

    # Creates a pattern that must match the whole string where a byte can be
    # matched any number of times
    rx_chars = re.compile(
        '^' +
        '(?:' +
        '|'.join([re.escape(c) for c in swift_charset_chars]) +
        ')*' +
        '$'
    )
    rx_nums = re.compile(
        '^' +
        '(?:' +
        '|'.join([re.escape(c) for c in swift_charset_numbers]) +
        ')*' +
        '$'
    )

    def __init__(self, locale='nl_NL'):
        if locale not in ('nl_NL',):
            raise ValueError("Locale not implemented: %s" % locale)

        self.locale = locale

        self._buffer = []


    # Convenience properties

    @property
    def type_char(self):
        return self.TYPE_CHARACTER

    @property
    def type_num(self):
        return self.TYPE_NUMERIC


    # "Immediate" API

    def serialize_value(self, type, maxlen, value, leading_zeroes=0):
        # Even if the value represents a number it could have leading zeros, so
        # we manipulate it as a bytestring
        if builtin_type(value) is not bytes:
            raise ValueError("Must pass a bytestring")

        if len(value) > maxlen:
            raise ValueError("Value cannot exceed %s bytes" % maxlen)

        if type == self.TYPE_CHARACTER and not self.rx_chars.match(value):
            raise ValueError("Character string value can only contain the bytes: %s"
                             % self.swift_charset_chars)

        if type == self.TYPE_NUMERIC and not self.rx_nums.match(value):
            raise ValueError("Numeric value can only contain the bytes: %s"
                             % self.swift_charset_numbers)

        if type == self.TYPE_NUMERIC and leading_zeroes:
            value = value.zfill(leading_zeroes)

        return value

    def serialize_newline(self):
        return b'\r\n'

    def serialize_amount(self, maxlen, currency, amount):
        if builtin_type(amount) is not Decimal:
            raise ValueError("Must pass a Decimal")

        # Amounts cannot have a negative sign
        if amount < Decimal('0'):
            raise ValueError(
                "Cannot serialize a negative amount, "
                "did you forget to use TYPE_DEBIT?")

        # FIXME: Decimal representation is currency and locale specific
        bytes = format_amount(amount, self.locale)

        # Now that we know how long the formatted bytestring is we can check
        # against maxlen
        if len(bytes) > maxlen:
            raise ValueError("Amount value exceeds maximum length: %s" % maxlen)

        return bytes

    def serialize_date(self, format, value):
        if builtin_type(value) is not datetime:
            raise ValueError("Must pass a datetime")

        return value.strftime(format)


    # Chaining API

    def start(self):
        self._buffer = []
        return self

    def finish(self):
        bytes = b''.join(self._buffer)
        self._buffer = []
        return bytes

    def newline(self):
        bytes = self.serialize_newline()
        self._buffer.append(bytes)
        return self

    # Generic values

    def chars(self, maxlen, value):
        bytes = self.serialize_value(self.TYPE_CHARACTER, maxlen, value)
        self._buffer.append(bytes)
        return self

    def chars_noslash(self, maxlen, value):
        if '/' in value:
            raise ValueError("Cannot use a slash here")

        return self.chars(maxlen, value)

    def num(self, maxlen, value, leading_zero=False):
        bytes = self.serialize_value(self.TYPE_NUMERIC, maxlen, value,
                                     leading_zeroes=maxlen if leading_zero else False)
        self._buffer.append(bytes)
        return self

    # Domain specific values

    def amount(self, maxlen, currency, amount):
        bytes = self.serialize_amount(maxlen, currency, amount)
        self._buffer.append(bytes)
        return self

    def date_yymmdd(self, date):
        bytes = self.serialize_date('%y%m%d', date)
        self._buffer.append(bytes)
        return self

    def date_mmdd(self, date):
        bytes = self.serialize_date('%m%d', date)
        self._buffer.append(bytes)
        return self
