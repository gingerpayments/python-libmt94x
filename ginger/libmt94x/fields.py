from datetime import datetime
from decimal import Decimal


# NOTE: Module level binding since we want to use the name "type" in method
# signatures
builtin_type = type


class Field(object):
    pass


class AbstractBalance(Field):
    tag = None

    TYPE_CREDIT = 1
    TYPE_DEBIT = 2

    def __init__(self, type, date, currency, amount):
        if type not in (self.TYPE_CREDIT, self.TYPE_DEBIT):
            raise ValueError("The `type` value must be TYPE_CREDIT or TYPE_DEBIT")

        if not builtin_type(date) == datetime:
            raise ValueError("The `date` value must be a datetime")

        if not builtin_type(amount) == Decimal:
            raise ValueError("The `amount` value must be a Decimal")

        self.type = type
        self.date = date
        self.currency = currency
        self.amount = amount



class AccountIdentification(Field):
    tag = '25'

    def __init__(self, iban, iso_currency_code):
        self.iban = iban
        self.iso_currency_code = iso_currency_code


class ClosingAvailableBalance(AbstractBalance):
    tag = '64'


class ClosingBalance(AbstractBalance):
    tag = '62F'


class ForwardAvailableBalance(AbstractBalance):
    tag = '65'


class InformationToAccountOwnerTotals(Field):
    tag = '86'

    def __init__(self, num_debit, num_credit, amount_debit, amount_credit):
        if not builtin_type(amount_debit) == Decimal:
            raise ValueError("The `amount_debit` value must be a Decimal")

        if not builtin_type(amount_credit) == Decimal:
            raise ValueError("The `amount_credit` value must be a Decimal")

        self.num_debit = num_debit
        self.num_credit = num_credit
        self.amount_debit = amount_debit
        self.amount_credit = amount_credit


class OpeningBalance(AbstractBalance):
    tag = '60F'


class StatementNumber(Field):
    tag = '28C'

    def __init__(self, statement_number):
        self.statement_number = statement_number


class TransactionReferenceNumber(Field):
    tag = '20'

    def __init__(self, transaction_reference_number):
        self.transaction_reference_number = transaction_reference_number
