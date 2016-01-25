from unittest import TestCase

from ginger.libmt94x.fields import AccountIdentification
from ginger.libmt94x.fields import StatementNumber
from ginger.libmt94x.fields import TransactionReferenceNumber
from ginger.libmt94x.serializer import Tm94xSerializer
from ginger.libmt94x.writer import Tm94xWriter


class Tm94xWriterTests(TestCase):
    def setUp(self):
        serializer = Tm94xSerializer()
        self.writer = Tm94xWriter(serializer)

    def test_account_identification(self):
        ai = AccountIdentification('NL69INGB0123456789', 'EUR')
        bytes = self.writer.write_account_identification(ai)
        self.assertEquals(bytes, b':25:NL69INGB0123456789EUR\r\n')

    def test_statement_number(self):
        sn = StatementNumber('00000')
        bytes = self.writer.write_statement_number(sn)
        self.assertEquals(bytes, b':28C:00000\r\n')

    def test_transaction_reference_number(self):
        trn = TransactionReferenceNumber('P140220000000001')
        bytes = self.writer.write_transaction_reference_number(trn)
        self.assertEquals(bytes, b':20:P140220000000001\r\n')
