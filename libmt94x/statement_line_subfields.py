from decimal import Decimal

from libmt94x.currency_codes import CurrencyCodes


class StatementLineSubField(object):
    '''Abstract base class for all subfields of StatementLine'''
    pass


class OriginalAmountOfTransaction(StatementLineSubField):
    def __init__(self, currency, amount):
        currency_codes = CurrencyCodes.get_instance()
        if not currency_codes.code_is_valid(currency):
            raise ValueError("Value `currency` is invalid: %s" % currency)

        if not type(amount) == Decimal:
            raise ValueError("The `amount` value must be a Decimal")

        self.currency = currency
        self.amount = amount
