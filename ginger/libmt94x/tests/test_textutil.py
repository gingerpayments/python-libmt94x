from unittest import TestCase

from ginger.libmt94x.textutil import break_at_width


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
