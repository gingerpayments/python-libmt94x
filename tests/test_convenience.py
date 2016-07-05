# -*- coding: utf-8 -*-

from unittest import TestCase
import random

from libmt94x.convenience import CharsetHelper
from libmt94x.serializer import Mt94xSerializer


def get_random_unicode_char(upper=0x10ffff):
    '''NOTE: 0 - 0x10ffff is the domain of unichr'''

    n = random.randrange(upper)
    return unichr(n)

def get_random_unicode_str(length, upper=None):
    chars = []
    for _ in xrange(length):
        char = get_random_unicode_char(upper=upper)
        chars.append(char)
    return u''.join(chars)


class ConvenienceTests(TestCase):
    def setUp(self):
        self.helper = CharsetHelper()
        self.serializer = Mt94xSerializer()

    def test_coerce_invalid_none(self):
        with self.assertRaises(ValueError):
            self.helper.coerce(None)

    def test_coerce_tolerate_empty(self):
        st = self.helper.coerce(b'')
        self.assertEquals(b'', st)

    def test_coerce_ascii(self):
        st = self.helper.coerce(b'abc')
        self.assertEquals(b'abc', st)

    def test_coerce_accented(self):
        st = self.helper.coerce(b'áéíóúüàèìòù')
        # Only the accents are stripped
        self.assertEquals(b'aeiouuaeiou', st)

    def test_coerce_ascii_disallowed(self):
        st = self.helper.coerce(b'a#b@c*d[]e%f><g^h=i_j"k&l;m')
        self.assertEquals(b'abcdefghijklm', st)

    def test_coerce_random_unicode_chars(self):
        # Includes the Basic Multilingual Plane
        # We don't want surrogate pairs since unidecode doesn't know how to
        # handle them
        codepoint_upper = 0xfff
        length = codepoint_upper

        # Generate completely arbitrary unicode chars
        st = get_random_unicode_str(length=length, upper=codepoint_upper)
        # Coerce it to something the serializer will accept
        st_ok = self.helper.coerce(st)

        # Coerced does not raise
        self.serializer.serialize_value(
            type=self.serializer.TYPE_CHARACTER,
            # NOTE: unidecode can expand a single unicode char to multiple chars, eg.
            # '®' -> '(r)'
            maxlen=codepoint_upper * 50,
            value=st_ok,
        )

        # Non-coerced does raise
        with self.assertRaises(ValueError):
            self.serializer.serialize_value(
                type=self.serializer.TYPE_CHARACTER,
                maxlen=codepoint_upper * 50,
                value=st,
            )
