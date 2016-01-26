from datetime import datetime
from decimal import Decimal

from ginger.libmt94x.transaction_codes import TransactionCodes


# NOTE: Module level binding since we want to use the name "type" in method
# signatures
builtin_type = type


class Field(object):
    '''Abstract base class for all fields'''
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


class InformationToAcccountOwner(Field):
    tag = '86'

    # TODO


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


class StatementLine(Field):
    tag = '61'

    TYPE_CREDIT = 1
    TYPE_DEBIT = 2

    def __init__(self,
                 value_date,
                 type,
                 amount,
                 transaction_code,
                 reference_for_account_owner,
                 supplementary_details=None,
                 book_date=None,
                 ing_transaction_code=None,
                 transaction_reference=None,
                 account_servicing_institutions_reference=None):
        '''
        EN/NL terms from specs:
        - value_date - Valutadatum
        - book_date - Boekdatum
        - type - Credit/debet
        - amount - Bedrag
        - transaction_code - Transactietype
        - reference_for_account_owner - Betalingskenmerk
        - ing_transaction_code - ING transactiecode
        - transaction_reference - Transactiereferentie
        - supplementary_details - Aanvullende gegevens

        Only MING:
        - book_date
        - transaction_reference

        Only IBP:
        - account_servicing_institutions_reference
        '''

        # TODO: Check that the right fields are set when adding this to an
        # actual TM94x document

        if not builtin_type(value_date) == datetime:
            raise ValueError("The `value_date` value must be a datetime")

        if book_date is not None and not builtin_type(book_date) == datetime:
            raise ValueError("The `book_date` value must be a datetime")

        if type not in (self.TYPE_CREDIT, self.TYPE_DEBIT):
            raise ValueError("The `type` value must be TYPE_CREDIT or TYPE_DEBIT")

        if not builtin_type(amount) == Decimal:
            raise ValueError("The `amount` value must be a Decimal")

        transaction_codes = TransactionCodes.get_instance()
        if not transaction_codes.code_is_valid(transaction_code):
            raise ValueError("Value `transaction_code` is invalid: %s" % transaction_code)

        # FIXME: check that ing_transaction_code is valid

        self.value_date = value_date
        self.type = type
        self.amount = amount
        self.transaction_code = transaction_code
        self.reference_for_account_owner = reference_for_account_owner
        self.supplementary_details = supplementary_details
        self.book_date = book_date
        self.ing_transaction_code = ing_transaction_code
        self.transaction_reference = transaction_reference
        self.account_servicing_institutions_reference = account_servicing_institutions_reference


class StatementNumber(Field):
    tag = '28C'

    def __init__(self, statement_number):
        self.statement_number = statement_number


class TransactionReferenceNumber(Field):
    tag = '20'

    def __init__(self, transaction_reference_number):
        self.transaction_reference_number = transaction_reference_number
