class Tm94xWriter(object):
    def __init__(self, serializer):
        self.ser = serializer

    def write_account_identification(self, ai):
        record = (self.ser
            .start()
            .chars(4, b':%s:' % ai.tag)
            .chars(35, b'%s%s' % (ai.iban, ai.iso_currency_code))
            .newline()
            .finish()
        )
        return record

    def write_statement_number(self, sn):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % sn.tag)
            .num(5, sn.statement_number)
            .newline()
            .finish()
        )
        return record

    def write_transaction_reference_number(self, trn):
        record = (self.ser
            .start()
            .chars(4, b':%s:' % trn.tag)
            .chars(16, trn.transaction_reference_number)
            .newline()
            .finish()
        )
        return record
