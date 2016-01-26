from ginger.libmt94x.remittance_info import AbstractRemittanceInfo


class InfoToAcccountOwnerSubField(object):
    '''Abstract base class for all subfields of InformationToAcccountOwner'''
    pass


class CounterPartyID(InfoToAcccountOwnerSubField):
    '''NL term: Tegenpartij ID'''

    tag = 'CNTP'

    def __init__(self, account_number, bic, name, city=None):
        self.account_number = account_number
        self.bic = bic
        self.name = name
        self.city = city


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


class MandateReference(InfoToAcccountOwnerSubField):
    '''NL term: Machtigingskenmerk'''
    
    tag = 'MARF'

    def __init__(self, mandate_reference):
        self.mandate_reference = mandate_reference


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

    def __init__(self, code, issuer, remittance_info):
        if not isinstance(remittance_info, AbstractRemittanceInfo):
            raise ValueError(
                "Value for `remittance_info` must be instance of AbstractRemittanceInfo")

        self.code = code
        self.issuer = issuer
        self.remittance_info = remittance_info


class ReturnReason(InfoToAcccountOwnerSubField):
    '''NL term: Uitval reden'''

    tag = 'RTRN'

    def __init__(self, reason_code):
        transfer_failed = TransferFailed()
        if not transfer_failed.code_is_valid(reason_code):
            raise ValueError("Value `reason_code` is invalid: %s" % reason_code)

        self.reason_code = reason_code


class UltimateCreditor(InfoToAcccountOwnerSubField):
    '''NL term: Uiteindelijke incassant'''

    tag = 'ULTC'

    def __init__(self, name, id):
        self.name = name
        self.id = id


class UltimateDebtor(InfoToAcccountOwnerSubField):
    '''NL term: Uiteindelijke geincasseerde'''

    tag = 'ULTD'

    def __init__(self, name, id):
        self.name = name
        self.id = id


class InfoToAcccountOwnerSubFieldOrder(object):
    # This is the order in which the fields must be written
    fields = (
        ReturnReason,
        EndToEndReference,
        PaymentInformationID,
        MandateReference,
        CreditorID,
        CounterPartyID,
        RemittanceInformation,
        PurposeCode,
        UltimateCreditor,
        UltimateDebtor,
    )

    @classmethod
    def get_field_classes(cls):
        return cls.fields
