class AbstractRemittanceInfo(object):
    '''Abstract base class for all remittance info classes.'''
    pass


class UnstructuredRemittanceInfo(AbstractRemittanceInfo):
    def __init__(self, remittance_info):
        self.remittance_info = remittance_info


class DutchStructuredRemittanceInfo(AbstractRemittanceInfo):
    def __init__(self, payment_reference):
        '''NL terms:
        - payment_reference - betalingskenmerk'''

        self.payment_reference = payment_reference


class IsoStructuredRemittanceInfo(AbstractRemittanceInfo):
    def __init__(self, iso_reference):
        self.iso_reference = iso_reference
