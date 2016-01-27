from decimal import Decimal


class StatementLineSubField(object):
    '''Abstract base class for all subfields of StatementLine'''
    pass


class OriginalAmountOfTransaction(StatementLineSubField):
    def __init__(self, currency, amount):
        if not type(amount) == Decimal:
            raise ValueError("The `amount` value must be a Decimal")

        self.currency = currency
        self.amount = amount
