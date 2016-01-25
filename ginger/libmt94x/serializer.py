import re


# NOTE: Module level binding since we want to use the name "type" in method
# signatures
builtin_type = type


class Tm94xSerializer(object):
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

    def __init__(self):
        self._buffer = []


    # Convenience properties

    @property
    def type_char(self):
        return self.TYPE_CHARACTER

    @property
    def type_num(self):
        return self.TYPE_NUMERIC


    # Public API

    def serialize_value(self, type, maxlen, value):
        # Even if the value represents a number it could have leading zeros, so
        # we manipulate it as a bytestring
        if builtin_type(value) != bytes:
            raise ValueError("Must pass a bytestring")

        if len(value) > maxlen:
            raise ValueError("Value cannot exceed %s bytes" % maxlen)

        if type == self.TYPE_CHARACTER and not self.rx_chars.match(value):
            raise ValueError("Character string value can only contain the bytes: %s"
                             % self.swift_charset_chars)

        if type == self.TYPE_NUMERIC and not self.rx_nums.match(value):
            raise ValueError("Numeric value can only contain the bytes: %s"
                             % self.swift_charset_numbers)

        return value

    def serialize_newline(self):
        return b'\r\n'


    # Chaining API

    def start(self):
        self._buffer = []
        return self

    def chars(self, maxlen, value):
        bytes = self.serialize_value(self.TYPE_CHARACTER, maxlen, value)
        self._buffer.append(bytes)
        return self

    def num(self, maxlen, value):
        bytes = self.serialize_value(self.TYPE_NUMERIC, maxlen, value)
        self._buffer.append(bytes)
        return self

    def newline(self):
        bytes = self.serialize_newline()
        self._buffer.append(bytes)
        return self

    def finish(self):
        bytes = b''.join(self._buffer)
        self._buffer = []
        return bytes
