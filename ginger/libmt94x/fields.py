from datetime import datetime
from decimal import Decimal

from ginger.libmt94x.info_acct_owner_subfields import InfoToAcccountOwnerSubField
from ginger.libmt94x.statement_line_subfields import OriginalAmountOfTransaction
from ginger.libmt94x.transaction_codes import IngTransactionCodes
from ginger.libmt94x.transaction_codes import SwiftTransactionCodes


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
            raise ValueError(
                "The `type` value must be TYPE_CREDIT or TYPE_DEBIT")

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


class ExportInformation(Field):
    '''This is part of the IBP header'''

    def __init__(self, export_address, export_number, export_time=None, export_day=None):
        self.export_address = export_address
        self.export_number = export_number
        self.export_time = export_time
        self.export_day = export_day


class ForwardAvailableBalance(AbstractBalance):
    tag = '65'


class ImportInformation(Field):
    '''This is part of the IBP header'''

    def __init__(self, import_address, import_number, import_time=None, import_day=None):
        self.import_address = import_address
        self.import_number = import_number
        self.import_time = import_time
        self.import_day = import_day


class InformationToAccountOwner(Field):
    tag = '86'

    def __init__(self, code_words=None, free_form_text=None):
        '''The parameters `code_words` and `free_form_text` are exclusively,
        meaning the content of this field is either structured (code_words) or
        unstructured.  The unstructured form is commonly used in the IBP
        dialect.'''

        if all((code_words, free_form_text)):
            raise ValueError("Only one of `code_words` or `free_form_text` may be provided")

        code_words = code_words or []

        for code_word in code_words:
            if not isinstance(code_word, InfoToAcccountOwnerSubField):
                raise ValueError(
                    "All values for `code_words` must be "
                    "instances of InfoToAcccountOwnerSubField")

        self.code_words = code_words
        self.free_form_text = free_form_text

        # Build dictionary mapping the class -> code_word
        by_class = {}
        for code_word in code_words:
            by_class[code_word.__class__] = code_word
        self.by_class = by_class

    def get_code_word_by_cls(self, cls_obj):
        return self.by_class.get(cls_obj)


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
                 account_servicing_institutions_reference=None,
                 original_amount_of_transaction=None):
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
        - original_amount_of_transaction
        '''

        if not builtin_type(value_date) == datetime:
            raise ValueError("The `value_date` value must be a datetime")

        if book_date is not None and not builtin_type(book_date) == datetime:
            raise ValueError("The `book_date` value must be a datetime")

        if type not in (self.TYPE_CREDIT, self.TYPE_DEBIT):
            raise ValueError("The `type` value must be TYPE_CREDIT or TYPE_DEBIT")

        if not builtin_type(amount) == Decimal:
            raise ValueError("The `amount` value must be a Decimal")

        swift_transaction_codes = SwiftTransactionCodes.get_instance()
        if not swift_transaction_codes.code_is_valid(transaction_code):
            raise ValueError(
                "Value `transaction_code` is invalid: %s" % transaction_code)

        if ing_transaction_code is not None:
            ing_transaction_codes = IngTransactionCodes.get_instance()
            if not ing_transaction_codes.code_is_valid(ing_transaction_code):
                raise ValueError(
                    "Value `ing_transaction_code` is invalid: %s" % ing_transaction_code)

        if (original_amount_of_transaction is not None and
            not builtin_type(original_amount_of_transaction) == OriginalAmountOfTransaction):
            raise ValueError("The `original_amount_of_transaction` value must "
                             "be an instance of OriginalAmountOfTransaction")

        self.value_date = value_date
        self.type = type
        self.amount = amount
        self.transaction_code = transaction_code
        self.reference_for_account_owner = reference_for_account_owner
        self.supplementary_details = supplementary_details  # not actually used
        self.book_date = book_date
        self.ing_transaction_code = ing_transaction_code
        self.transaction_reference = transaction_reference
        self.account_servicing_institutions_reference = account_servicing_institutions_reference
        self.original_amount_of_transaction = original_amount_of_transaction


class StatementNumber(Field):
    tag = '28C'

    def __init__(self, statement_number):
        self.statement_number = statement_number


class TransactionReferenceNumber(Field):
    tag = '20'

    def __init__(self, transaction_reference_number=None):
        self.transaction_reference_number = transaction_reference_number
