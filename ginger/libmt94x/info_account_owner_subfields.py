from ginger.libmt94x.transfer_failed_reasons import AbstractTransferFailed


class InfoToAcccountOwnerSubField(object):
    '''Abstract base class for all subfields of InformationToAcccountOwner'''
    pass


class CounterPartyID(InfoToAcccountOwnerSubField):
    '''NL term: Tegenpartij ID'''

    code_word = 'CNTP'

    def __init__(self, account_number, bic, name, city):
        self.account_number = account_number
        self.bic = bic
        self.name = name
        self.city = city


class CreditorID(InfoToAcccountOwnerSubField):
    '''NL term: Incassant ID'''

    code_word = 'CSID'

    def __init__(self, creditor_id):
        self.creditor_id = creditor_id


class EndToEndReference(InfoToAcccountOwnerSubField):
    '''NL term: Uniek kenmerk'''

    code_word = 'EREF'

    def __init__(self, end_to_end_reference):
        self.end_to_end_reference = end_to_end_reference


class MandateReference(InfoToAcccountOwnerSubField):
    '''NL term: Machtigingskenmerk'''
    
    code_word = 'MARF'

    def __init__(self, mandate_reference):
        self.mandate_reference = mandate_reference


class PaymentInformationID(InfoToAcccountOwnerSubField):
    '''NL term: Batch ID'''

    code_word = 'PREF'

    def __init__(self, payment_information_id):
        self.payment_information_id = payment_information_id


class PurposeCode(InfoToAcccountOwnerSubField):
    '''NL term: Speciale verwerkingscode'''

    code_word = 'PURP'

    def __init__(self, purpose_of_collection):
        self.purpose_of_collection = purpose_of_collection


class RemittanceInformation(InfoToAcccountOwnerSubField):
    '''NL term: Omschrijvingsregels'''

    code_word = 'REMI'

    def __init__(self, code, issuer, remittance_info, purpose_of_collection):
        self.code = code
        self.issuer = issuer
        self.remittance_info = remittance_info  # TODO: this is structured data
        self.purpose_of_collection = purpose_of_collection


class ReturnReason(InfoToAcccountOwnerSubField):
    '''NL term: Uitval reden'''

    code_word = 'RTRN'

    def __init__(self, reason_code):
        transfer_failed = TransferFailed()
        if not transfer_failed.code_is_valid(reason_code):
            raise ValueError("Value `reason_code` is invalid: %s" % reason_code)

        self.reason_code = reason_code


class UltimateCreditor(InfoToAcccountOwnerSubField):
    '''NL term: Uiteindelijke incassant'''

    code_word = 'ULTC'

    def __init__(self, name, id):
        self.name = name
        self.id = id


class UltimateDebitor(InfoToAcccountOwnerSubField):
    '''NL term: Uiteindelijke geincasseerde'''

    code_word = 'ULTD'

    def __init__(self, name, id):
        self.name = name
        self.id = id
