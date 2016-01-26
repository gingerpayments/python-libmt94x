class InvalidTransactionCodeError(Exception):
    pass


class TransactionCodes(object):
    '''De volgende SWIFT transactietypen worden gebruikt voor ING rekeningen.
    Een volledige lijst met SWIFT transactietypen vindt u op www.swift.com.
    SWIFT transactietypen beginnen met de letter "N" gevolgd door de
    ISO-code.'''

    # iso code -> description
    codes = {
        'BNK': 'Securities Related Item - Bank fees',
        'BOE': 'Bill of exchange',
        'BRF': 'Brokerage fee',
        'CAR': 'Securities Related Item - Corporate Actions Related',
        'CAS': 'Securities Related Item - Cash in Lieu',
        'CHG': 'Charges and other expenses',
        'CHK': 'Cheques',
        'CLR': 'Cash letters/Cheques remittance',
        'CMI': 'Cash management item - No detail',
        'CMN': 'Cash management item - Notional pooling',
        'CMP': 'Compensation claims',
        'CMS': 'Cash management item - Sweeping',
        'CMT': 'Cash management item -Topping',
        'CMZ': 'Cash management item - Zero balancing',
        'COL': 'Collections (used when entering a principal amount)',
        'COM': 'Commission',
        'CPN': 'Securities Related Item - Coupon payments',
        'DCR': 'Documentary credit (used when entering a principal amount)',
        'DDT': 'Direct Debit Item',
        'DIS': 'Securities Related Item - Gains disbursement',
        'DIV': 'Securities Related Item - Dividends',
        'EQA': 'Equivalent amount',
        'EXT': 'Securities Related Item - External transfer for own account',
        'FEX': 'Foreign exchange',
        'INT': 'Interest',
        'LBX': 'Lock box',
        'LDP': 'Loan deposit',
        'MAR': 'Securities Related Item - Margin payments/Receipts',
        'MAT': 'Securities Related Item - Maturity',
        'MGT': 'Securities Related Item - Management fees',
        'MSC': 'Miscellaneous',
        'NWI': 'Securities Related Item - New issues distribution',
        'ODC': 'Overdraft charge',
        'OPT': 'Securities Related Item - Options',
        'PCH': 'Securities Related Item - Purchase',
        'POP': 'Securities Related Item - Pair-off proceeds',
        'PRN': 'Securities Related Item - Principal pay-down/pay-up',
        'REC': 'Securities Related Item - Tax reclaim',
        'RED': 'Securities Related Item - Redemption/Withdrawal',
        'RIG': 'Securities Related Item - Rights',
        'RTI': 'Returned item',
        'SAL': 'Securities Related Item - Sale',
        'SEC': 'Securities (used when entering a principal amount)',
        'SLE': 'Securities Related Item - Securities lending related',
        'STO': 'Standing order',
        'STP': 'Securities Related Item - Stamp duty',
        'SUB': 'Securities Related Item - Subscription',
        'SWP': 'Securities',
        'TAX': 'Securities Related Item - Withholding tax payment',
        'TCK': 'Travelers cheques',
        'TCM': 'Securities Related Item - Tripartite collateral management',
        'TRA': 'Securities Related Item - Internal transfer for own account',
        'TRF': 'Transfer',
        'TRN': 'Securities Related Item - Transaction fee',
        'UWC': 'Securities Related Item - Underwriting commission',
        'VDA': 'Value date adjustment',
        'WAR': 'Securities Related Item - Warrant',
    }
    instance = None

    @classmethod
    def get_instance(cls):
        '''This class stores no state, so we can store a global instance in the
        class and give it out on demand.'''

        if cls.instance is None:
            cls.instance = cls()

        return cls.instance

    def code_is_valid(self, code):
        try:
            self.resolve_code(code)
            return True
        except InvalidTransactionCodeError:
            return False

    def resolve_code(self, code):
        try:
            return self.codes[code]
        except KeyError:
            raise InvalidTransactionCodeError("Code not found: %s" % code)
