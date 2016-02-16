from decimal import Decimal
from unittest import TestCase

from ginger_libmt94x.textutil import break_at_width
from ginger_libmt94x.textutil import format_amount


class TextUtilTests(TestCase):
    def test_break_at_width(self):
        line = (
            b':86:/EREF/500411584454//MARF/1.15791632//CSID/NL93ZZZ332656790051'
            b'//CNTP/NL12COBA0733959555/COBANL2XXXX/T-Mobile Netherlands BV///R'
            b'EMI/USTD//Factuurnummer 901258406560//PURP/OTHR/'
        )
        expected = (
            b':86:/EREF/500411584454//MARF/1.15791632//CSID/NL93ZZZ332656790051\r\n'
            b'//CNTP/NL12COBA0733959555/COBANL2XXXX/T-Mobile Netherlands BV///R\r\n'
            b'EMI/USTD//Factuurnummer 901258406560//PURP/OTHR/'
        )

        block = break_at_width(line, width=65, newline='\r\n')
        self.assertEquals(block, expected)

    def test_break_at_width_no_double_newline(self):
        # Length: 130 chars + newline
        line = (
            b'500411584454 1.15791632 NL93ZZZ332656790051 NL12COBA0733959555 CO'
            b'BANL2XXXX T-Mobile Netherlands BV Factuurnummer 901258406560 OTHR\r\n'
        )
        expected = (
            b'500411584454 1.15791632 NL93ZZZ332656790051 NL12COBA0733959555 CO\r\n'
            b'BANL2XXXX T-Mobile Netherlands BV Factuurnummer 901258406560 OTHR\r\n'
        )

        block = break_at_width(line, width=65, newline='\r\n')
        self.assertEquals(block, expected)

    def test_format_amount_nl(self):
        rv = format_amount(Decimal('1.23'), locale='nl_NL')
        self.assertEquals('1,23', rv)

    def test_format_amount_fr(self):
        with self.assertRaises(NotImplementedError):
            format_amount(Decimal('1.23'), locale='fr_FR')
