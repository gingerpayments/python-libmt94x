from libmt94x.remittance_info import AbstractRemittanceInfo
from libmt94x.transfer_failed_codes import TransferFailed


class InfoToAcccountOwnerSubField(object):
    '''Abstract base class for all subfields of InformationToAcccountOwner'''
    pass


class BeneficiaryParty(InfoToAcccountOwnerSubField):
    tag = 'BENM'

    def __init__(self, account_number=None, bic=None, name=None, city=None):
        self.account_number = account_number
        self.bic = bic
        self.name = name
        self.city = city


class BusinessPurpose(InfoToAcccountOwnerSubField):
    tag = 'BUSP'

    def __init__(self, id_code=None, sepa_transaction_type=None):
        self.id_code = id_code
        self.sepa_transaction_type = sepa_transaction_type


class Charges(InfoToAcccountOwnerSubField):
    tag = 'CHGS'

    def __init__(self, charges):
        self.charges = charges


class ClientReference(InfoToAcccountOwnerSubField):
    tag = 'CREF'

    def __init__(self, client_reference):
        self.client_reference = client_reference


class CounterPartyID(InfoToAcccountOwnerSubField):
    '''NL term: Tegenpartij ID'''

    tag = 'CNTP'

    def __init__(self, account_number=None, bic=None, name=None, city=None):
        self.account_number = account_number
        self.bic = bic
        self.name = name
        self.city = city


class CounterPartyIdentification(InfoToAcccountOwnerSubField):
    tag = 'ID'

    def __init__(self, id_code):
        self.id_code = id_code


class CreditorID(InfoToAcccountOwnerSubField):
    '''NL term: Incassant ID'''

    tag = 'CSID'

    def __init__(self, creditor_id):
        self.creditor_id = creditor_id


class EndToEndReference(InfoToAcccountOwnerSubField):
    '''NL term: Uniek kenmerk'''

    tag = 'EREF'

    def __init__(self, end_to_end_reference):
        self.end_to_end_reference = end_to_end_reference


class ExchangeRate(InfoToAcccountOwnerSubField):
    tag = 'EXCH'

    def __init__(self, exchange_rate):
        self.exchange_rate = exchange_rate


class InstructionID(InfoToAcccountOwnerSubField):
    tag = 'IREF'

    def __init__(self, instruction_id):
        self.instruction_id = instruction_id


class MandateReference(InfoToAcccountOwnerSubField):
    '''NL term: Machtigingskenmerk'''

    tag = 'MARF'

    def __init__(self, mandate_reference):
        self.mandate_reference = mandate_reference


class OrderingParty(InfoToAcccountOwnerSubField):
    tag = 'ORDP'

    def __init__(self, account_number=None, bic=None, name=None, city=None):
        self.account_number = account_number
        self.bic = bic
        self.name = name
        self.city = city


class PaymentInformationID(InfoToAcccountOwnerSubField):
    '''NL term: Batch ID'''

    tag = 'PREF'

    def __init__(self, payment_information_id):
        self.payment_information_id = payment_information_id


class PurposeCode(InfoToAcccountOwnerSubField):
    '''NL term: Speciale verwerkingscode'''

    tag = 'PURP'

    def __init__(self, purpose_of_collection):
        self.purpose_of_collection = purpose_of_collection


class RemittanceInformation(InfoToAcccountOwnerSubField):
    '''NL term: Omschrijvingsregels'''

    tag = 'REMI'

    def __init__(self, remittance_info, code=None, issuer=None):
        if not isinstance(remittance_info, AbstractRemittanceInfo):
            raise ValueError(
                "Value for `remittance_info` must be instance of AbstractRemittanceInfo")

        self.remittance_info = remittance_info

        # TODO: Are these two even used??? They are in the spec but do not
        # appear in examples
        self.code = code
        self.issuer = issuer


class ReturnReason(InfoToAcccountOwnerSubField):
    '''NL term: Uitval reden'''

    tag = 'RTRN'

    def __init__(self, reason_code):
        '''NOTE: The ING IBP spec also mentions a legacy R-Type integer
        parameter which has the following possible values:
            1 - Reject (geweigerde)
            2 - Return (retourbetaling)
            3 - Refund (terugbetaling)
            4 - Reversal (herroeping)
            5 - Cancellation (annulering)

        The R-Type is concatenated to the `reason_code`. We do not implement the R-Type,
        we just mention it here for reference.'''

        transfer_failed = TransferFailed.get_instance()
        if not transfer_failed.code_is_valid(reason_code):
            raise ValueError("Value `reason_code` is invalid: %s" % reason_code)

        self.reason_code = reason_code


class UltimateBeneficiary(InfoToAcccountOwnerSubField):
    tag = 'ULTB'

    def __init__(self, name):
        self.name = name


class UltimateCreditor(InfoToAcccountOwnerSubField):
    '''NL term: Uiteindelijke incassant'''

    tag = 'ULTC'

    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id


class UltimateDebtor(InfoToAcccountOwnerSubField):
    '''NL term: Uiteindelijke geincasseerde'''

    tag = 'ULTD'

    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id


class InfoToAcccountOwnerSubFieldOrder(object):
    # This is the order in which the fields must be written
    fields = (
        ReturnReason,
        BusinessPurpose,
        ClientReference,
        EndToEndReference,
        PaymentInformationID,
        InstructionID,
        MandateReference,
        CreditorID,
        CounterPartyID,
        BeneficiaryParty,
        OrderingParty,
        RemittanceInformation,
        CounterPartyIdentification,
        PurposeCode,
        UltimateBeneficiary,
        UltimateCreditor,
        UltimateDebtor,
        ExchangeRate,
        Charges,
    )

    @classmethod
    def get_field_classes(cls):
        return cls.fields
