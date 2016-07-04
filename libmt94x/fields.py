from datetime import datetime
from decimal import Decimal

from libmt94x.currency_codes import CurrencyCodes
from libmt94x.info_acct_owner_subfields import BeneficiaryParty
from libmt94x.info_acct_owner_subfields import BusinessPurpose
from libmt94x.info_acct_owner_subfields import Charges
from libmt94x.info_acct_owner_subfields import ClientReference
from libmt94x.info_acct_owner_subfields import CounterPartyID
from libmt94x.info_acct_owner_subfields import CounterPartyIdentification
from libmt94x.info_acct_owner_subfields import CreditorID
from libmt94x.info_acct_owner_subfields import EndToEndReference
from libmt94x.info_acct_owner_subfields import ExchangeRate
from libmt94x.info_acct_owner_subfields import InfoToAcccountOwnerSubField
from libmt94x.info_acct_owner_subfields import InstructionID
from libmt94x.info_acct_owner_subfields import MandateReference
from libmt94x.info_acct_owner_subfields import OrderingParty
from libmt94x.info_acct_owner_subfields import PaymentInformationID
from libmt94x.info_acct_owner_subfields import PurposeCode
from libmt94x.info_acct_owner_subfields import RemittanceInformation
from libmt94x.info_acct_owner_subfields import ReturnReason
from libmt94x.info_acct_owner_subfields import UltimateBeneficiary
from libmt94x.info_acct_owner_subfields import UltimateCreditor
from libmt94x.info_acct_owner_subfields import UltimateDebtor
from libmt94x.remittance_info import DutchStructuredRemittanceInfo
from libmt94x.remittance_info import IsoStructuredRemittanceInfo
from libmt94x.remittance_info import UnstructuredRemittanceInfo
from libmt94x.statement_line_subfields import OriginalAmountOfTransaction
from libmt94x.transaction_codes import IngTransactionCodes
from libmt94x.transaction_codes import SwiftTransactionCodes


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

        if not builtin_type(date) is datetime:
            raise ValueError("The `date` value must be a datetime")

        currency_codes = CurrencyCodes.get_instance()
        if not currency_codes.code_is_valid(currency):
            raise ValueError("Value `currency` is invalid: %s" % currency)

        if not builtin_type(amount) is Decimal:
            raise ValueError("The `amount` value must be a Decimal")

        self.type = type
        self.date = date
        self.currency = currency
        self.amount = amount



class AccountIdentification(Field):
    tag = '25'

    def __init__(self, iban, iso_currency_code=None):
        currency_codes = CurrencyCodes.get_instance()
        if (iso_currency_code is not None and
            not currency_codes.code_is_valid(iso_currency_code)):
            raise ValueError(
                "Value `iso_currency_code` is invalid: %s" % iso_currency_code)

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
        '''The parameters `code_words` and `free_form_text` are exclusive,
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

    def flatten(self):
        '''Transform code_words to free_form_text of values delimited by a
        space (from IBP structured to IBP unstructured). Note that this is a
        destructive update.'''

        def maybe_add(elems, value):
            if value:
                elems.append(value)

        elems = []
        for code_word in self.code_words:
            if isinstance(code_word, BeneficiaryParty):
                maybe_add(elems, code_word.account_number)
                maybe_add(elems, code_word.bic)
                maybe_add(elems, code_word.name)
                maybe_add(elems, code_word.city)
            elif isinstance(code_word, BusinessPurpose):
                maybe_add(elems, code_word.id_code)
                maybe_add(elems, code_word.sepa_transaction_type)
            elif isinstance(code_word, Charges):
                maybe_add(elems, code_word.charges)
            elif isinstance(code_word, ClientReference):
                maybe_add(elems, code_word.client_reference)
            elif isinstance(code_word, CounterPartyID):
                maybe_add(elems, code_word.account_number)
                maybe_add(elems, code_word.bic)
                maybe_add(elems, code_word.name)
                maybe_add(elems, code_word.city)
            elif isinstance(code_word, CounterPartyIdentification):
                maybe_add(elems, code_word.id_code)
            elif isinstance(code_word, CreditorID):
                maybe_add(elems, code_word.creditor_id)
            elif isinstance(code_word, EndToEndReference):
                maybe_add(elems, code_word.end_to_end_reference)
            elif isinstance(code_word, ExchangeRate):
                maybe_add(elems, code_word.exchange_rate)
            elif isinstance(code_word, InstructionID):
                maybe_add(elems, code_word.instruction_id)
            elif isinstance(code_word, MandateReference):
                maybe_add(elems, code_word.mandate_reference)
            elif isinstance(code_word, OrderingParty):
                maybe_add(elems, code_word.account_number)
                maybe_add(elems, code_word.bic)
                maybe_add(elems, code_word.name)
                maybe_add(elems, code_word.city)
            elif isinstance(code_word, PaymentInformationID):
                maybe_add(elems, code_word.payment_information_id)
            elif isinstance(code_word, PurposeCode):
                maybe_add(elems, code_word.purpose_of_collection)
            elif isinstance(code_word, RemittanceInformation):
                if isinstance(code_word.remittance_info, UnstructuredRemittanceInfo):
                    maybe_add(elems, code_word.remittance_info.remittance_info)
                elif isinstance(code_word.remittance_info, DutchStructuredRemittanceInfo):
                    maybe_add(elems, code_word.remittance_info.payment_reference)
                elif isinstance(code_word.remittance_info, IsoStructuredRemittanceInfo):
                    maybe_add(elems, code_word.remittance_info.iso_reference)
            elif isinstance(code_word, ReturnReason):
                maybe_add(elems, code_word.reason_code)
            elif isinstance(code_word, UltimateBeneficiary):
                maybe_add(elems, code_word.name)
            elif isinstance(code_word, UltimateCreditor):
                maybe_add(elems, code_word.name)
                maybe_add(elems, code_word.id)
            elif isinstance(code_word, UltimateDebtor):
                maybe_add(elems, code_word.name)
                maybe_add(elems, code_word.id)

        line = ' '.join(elems)

        self.free_form_text = line
        self.code_words = []

    def get_code_word_by_cls(self, cls_obj):
        return self.by_class.get(cls_obj)


class InformationToAccountOwnerTotals(Field):
    tag = '86'

    def __init__(self, num_debit, num_credit, amount_debit, amount_credit):
        if not builtin_type(num_debit) is int:
            raise ValueError("The `num_debit` value must be an int")

        if not builtin_type(num_credit) is int:
            raise ValueError("The `num_credit` value must be an int")

        if not builtin_type(amount_debit) is Decimal:
            raise ValueError("The `amount_debit` value must be a Decimal")

        if not builtin_type(amount_credit) is Decimal:
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

        if not builtin_type(value_date) is datetime:
            raise ValueError("The `value_date` value must be a datetime")

        if book_date is not None and not builtin_type(book_date) is datetime:
            raise ValueError("The `book_date` value must be a datetime")

        if type not in (self.TYPE_CREDIT, self.TYPE_DEBIT):
            raise ValueError("The `type` value must be TYPE_CREDIT or TYPE_DEBIT")

        if not builtin_type(amount) is Decimal:
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
            not builtin_type(original_amount_of_transaction) is OriginalAmountOfTransaction):
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
