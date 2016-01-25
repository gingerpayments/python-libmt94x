class Field(object):
    pass


class AccountIdentification(Field):
    tag = '25'

    def __init__(self, iban, iso_currency_code):
        self.iban = iban
        self.iso_currency_code = iso_currency_code


class StatementNumber(Field):
    tag = '28C'

    def __init__(self, statement_number):
        self.statement_number = statement_number


class TransactionReferenceNumber(Field):
    tag = '20'

    def __init__(self, transaction_reference_number):
        self.transaction_reference_number = transaction_reference_number
