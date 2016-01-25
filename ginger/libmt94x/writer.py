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

    def write_closing_available_balance(self, cab):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % cab.tag)
            .chars(1, b'C' if cab.type == cab.TYPE_CREDIT else b'D')
            .date_yymmdd(cab.date)
            .chars(3, cab.currency)
            .amount(15, cab.currency, cab.amount)
            .newline()
            .finish()
        )
        return record

    def write_closing_balance(self, cb):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % cb.tag)
            .chars(1, b'C' if cb.type == cb.TYPE_CREDIT else b'D')
            .date_yymmdd(cb.date)
            .chars(3, cb.currency)
            .amount(15, cb.currency, cb.amount)
            .newline()
            .finish()
        )
        return record

    def write_forward_available_balance(self, fab):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % fab.tag)
            .chars(1, b'C' if fab.type == fab.TYPE_CREDIT else b'D')
            .date_yymmdd(fab.date)
            .chars(3, fab.currency)
            .amount(15, fab.currency, fab.amount)
            .newline()
            .finish()
        )
        return record

    def write_information_to_account_owner_totals_ibp(self, info):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % info.tag)
            .chars(1, b'D')
            .num(6, b'%s' % info.num_debit)
            .chars(1, b'C')
            .num(6, b'%s' % info.num_credit)
            .chars(1, b'D')
            .amount(15, None, info.amount_debit)
            .chars(1, b'C')
            .amount(15, None, info.amount_credit)
            .newline()
            .finish()
        )
        return record

    def write_information_to_account_owner_totals_ming(self, info):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % info.tag)
            .chars(5, b'/SUM/')
            .num(6, b'%s' % info.num_debit)
            .chars(1, b'/')
            .num(6, b'%s' % info.num_credit)
            .chars(1, b'/')
            .amount(15, None, info.amount_debit)
            .chars(1, b'/')
            .amount(15, None, info.amount_credit)
            .chars(1, b'/')
            .newline()
            .finish()
        )
        return record

    def write_opening_balance(self, ob):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % ob.tag)
            .chars(1, b'C' if ob.type == ob.TYPE_CREDIT else b'D')
            .date_yymmdd(ob.date)
            .chars(3, ob.currency)
            .amount(15, ob.currency, ob.amount)
            .newline()
            .finish()
        )
        return record

    def write_statement_line_ibp(self, sl):
        record = (self.ser
            .start()
            .chars(4, b':%s:' % sl.tag)
            .date_yymmdd(sl.value_date)
            .chars(1, b'C' if sl.type == sl.TYPE_CREDIT else b'D')
            .amount(15, None, sl.amount)
            .chars(4, b'N%s' % sl.transaction_code)
            .chars(16, sl.reference_for_account_owner or b'NONREF')
            .chars(16, sl.account_servicing_institutions_reference)  # FIXME: optional
            # Supplementary Details
            .chars(34, b'/TRCD/%s/' % sl.ing_transaction_code)
            # FIXME: /OCMT/USD1234,50/
            .newline()
            .finish()
        )
        return record

    def write_statement_line_ming(self, sl):
        record = (self.ser
            .start()
            .chars(4, b':%s:' % sl.tag)
            .date_yymmdd(sl.value_date)
            .date_mmdd(sl.book_date)
            .chars(1, b'C' if sl.type == sl.TYPE_CREDIT else b'D')
            .amount(15, None, sl.amount)
            .chars(4, b'N%s' % sl.transaction_code)
            .chars(16, sl.reference_for_account_owner or b'NONREF')
            .chars(16, b'//%s' % sl.transaction_reference)
            .newline()
            .chars(34, b'/TRCD/%s/' % sl.ing_transaction_code)
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
