import re

from unidecode import unidecode

from libmt94x.serializer import Mt94xSerializer


class CharsetHelper(object):
    # Like Mt94xSerializer.swift_charset_chars but exclusive
    rx_chars_ex = re.compile(
        '[^' +
        ''.join([re.escape(c) for c in Mt94xSerializer.swift_charset_chars]) +
        ']*'
    )

    def coerce(self, st):
        '''Strips out any characters outside the SWIFT character set.'''

        # Do not accept a None value (probably an error in the caller)
        if st is None:
            raise ValueError("Must pass a string")

        # Return the empty string
        if not st:
            return st

        # Translate accented characters to ascii equivalents (unidecode
        # requires unicode value)
        if type(st) is bytes:
            st = st.decode('utf-8')

        st = unidecode(st)

        # Strip out all characters not in the SWIFT charset
        st = self.rx_chars_ex.sub('', st)

        # Make sure we emit bytes
        if type(st) is unicode:
            st = st.encode('utf-8')

        return st
