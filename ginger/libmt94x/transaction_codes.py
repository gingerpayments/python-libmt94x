class InvalidIngTransactionCodeError(Exception):
    pass


class InvalidSwiftTransactionCodeError(Exception):
    pass


class AbstractTransactionCodes(object):
    '''This is an abstract class for all transaction codes classes.'''

    instance = None

    @classmethod
    def get_instance(cls):
        '''This class stores no state, so we can store a global instance in the
        class and give it out on demand.'''

        if cls.instance is None:
            cls.instance = cls()

        return cls.instance

    def code_is_valid(self, code):
        raise NotImplementedError

    def resolve_code(self, code):
        raise NotImplementedError


class IngTransactionCodes(AbstractTransactionCodes):
    '''These are ING transaction codes

    From the spec:
    De volgende specifieke ING transactiecodes worden gebruikt voor ING
    rekeningen.  Deze lijst kan in de toekomst worden aangevuld met nieuwe ING
    transactiecodes.'''

    codes = {
        '00000': 'Miscellaneous',
        '00100': 'SEPA Credit Transfer',
        '00101': 'SEPA Credit Transfer (paper based)',
        '00102': 'SEPA Credit Transfer (Intracompany)',
        '00103': 'European Credit Transfer',
        '00104': 'SEPA Standing Order',
        '00106': 'SEPA iDEAL payment',
        '00107': 'SEPA E-invoice payment (FINBOX)',
        '00108': 'IBAN Acceptgiro',
        '00150': 'SEPA Credit Transfer (Urgent)',
        '00170': 'SEPA Credit Transfer (loan pay-off)',
        '00190': 'Return SEPA Credit Transfer',
        '00192': 'Return SEPA Credit Transfer (Intracompany)',
        '00193': 'Return SEPA Credit Transfer (Urgent)',
        '00196': 'Return iDEAL',
        '00200': 'SEPA Multiple Credit Transfer',
        '00201': 'SEPA Credit Transfer',
        '00202': 'SEPA Multiple Credit Transfer Salary Batch',
        '00203': 'SEPA Credit Transfer (Salary)',
        '00206': 'iDEAL merchant payment',
        '00207': 'iDEAL payment',
        '00250': 'Reject Domestic Multiple Credit Transfer',
        '00291': 'Return Salary Payment',
        '00300': 'Domestic Credit Transfer',
        '00301': 'Domestic Credit Transfer (paper)',
        '00302': 'Domestic Credit Transfer (phone)',
        '00303': 'Domestic Credit Transfer (counter)',
        '00304': 'Domestic Standing Order',
        '00305': 'Domestic iDEAL payment',
        '00306': 'Domestic E-invoice payment (FINBOX)',
        '00350': 'Domestic Urgent Credit Transfer',
        '00351': 'Domestic Urgent Credit Transfer (fax)',
        '00353': 'Domestic Urgent Credit (counter)',
        '00360': 'Acceptgiro',
        '00361': 'Acceptgiro Storting',
        '00370': 'Domestic Credit Transfer from/to Savings account',
        '00371': 'Domestic Credit Transfer (loan pay-off)',
        '00390': 'Domestic Credit Transfer (return)',
        '00393': 'Domestic Standing Order (return)',
        '00395': 'iDEAL (return)',
        '00396': 'Acceptgiro (return)',
        '00400': 'Domestic Multiple Credit Transfer',
        '00401': 'Domestic Multiple Credit Transfer item',
        '00500': 'True International Payment',
        '00501': 'True International Payment (shared)',
        '00502': 'True International Payment (our)',
        '00503': 'True International Payment (beneficiary)',
        '00510': 'True International Payment counter',
        '00511': 'True International Payment SHA (paper)',
        '00512': 'True International Payment OUR (paper)',
        '00513': 'True International Payment BEN (paper)',
        '00550': 'True International Payment (prio)',
        '00590': 'Correction True International Payment',
        '01000': 'SEPA Direct Debit Batch',
        '01001': 'SEPA Direct Debit',
        '01010': 'SEPA Direct Debit Batch - Core',
        '01011': 'SEPA Core Direct Debit item- One Off',
        '01012': 'SEPA Core Direct Debit item - First',
        '01013': 'SEPA Core Direct Debit item - Recurrent',
        '01014': 'SEPA Core Direct Debit item - Last',
        '01015': 'SEPA Direct Debit - Core',
        '01016': 'SEPA Direct Debit - Core One Off',
        '01017': 'SEPA Direct Debit - Core First',
        '01018': 'SEPA Direct Debit - Core Recurrent',
        '01019': 'SEPA Direct Debit - Core Last',
        '01020': 'SEPA Direct Debit Batch - B2B',
        '01021': 'SEPA B2B Direct Debit item - One Off',
        '01022': 'SEPA B2B Direct Debit item - First',
        '01023': 'SEPA B2B Direct Debit item - Recurrent',
        '01024': 'SEPA B2B Direct Debit item - Last',
        '01025': 'SEPA Direct Debit - B2B',
        '01026': 'SEPA Direct Debit - B2B One Off',
        '01027': 'SEPA Direct Debit - B2B First',
        '01028': 'SEPA Direct Debit - B2B Recurrent',
        '01029': 'SEPA Direct Debit - B2B Last',
        '01036': 'SEPA Direct Debit - One Off',
        '01037': 'SEPA Direct Debit - First',
        '01038': 'SEPA Direct Debit - Recurrent',
        '01039': 'SEPA Direct Debit - Last',
        '01040': 'SEPA Direct Debit Batch - Cor1',
        '01045': 'SEPA Direct Debit - Cor1',
        '01046': 'SEPA Direct Debit - Cor1 One Off',
        '01047': 'SEPA Direct Debit - Cor1 First',
        '01048': 'SEPA Direct Debit - Cor1 Recurrent',
        '01049': 'SEPA Direct Debit - Cor1 Last',
        '01050': 'Domestic Direct Debit batch',
        '01051': 'Domestic Direct Debit item',
        '01061': 'Domestic Direct Debit batch (Government)',
        '01062': 'Domestic Direct Debit (Government)',
        '01090': 'Domestic Direct Debit Batch Reject',
        '01100': 'SEPA Direct Debit Batch Reject',
        '01101': 'SEPA Direct Debit Reject',
        '01102': 'SEPA Direct Debit One Off Reject',
        '01103': 'SEPA Direct Debit First Reject',
        '01104': 'SEPA Direct Debit Recurrent Reject',
        '01105': 'SEPA Direct Debit Last Reject',
        '01111': 'SEPA Direct Debit Core One Off Reject',
        '01112': 'SEPA Direct Debit Core First Reject',
        '01113': 'SEPA Direct Debit Core Recurrent Reject',
        '01114': 'SEPA Direct Debit Core Last Reject',
        '01115': 'SEPA Direct Debit Core Reject',
        '01125': 'SEPA Direct Debit B2B Reject',
        '01126': 'SEPA Direct Debit B2B One Off Reject',
        '01127': 'SEPA Direct Debit B2B First Reject',
        '01128': 'SEPA Direct Debit B2B Recurrent Reject',
        '01129': 'SEPA Direct Debit B2B Last Reject',
        '01150': 'Domestic Direct Debit Reject',
        '01201': 'SEPA Direct Debit Return',
        '01202': 'SEPA Direct Debit One Off Return',
        '01203': 'SEPA Direct Debit First Return',
        '01204': 'SEPA Direct Debit Recurrent Return',
        '01205': 'SEPA Direct Debit Last Return',
        '01216': 'SEPA Direct Debit Core One Off Return',
        '01217': 'SEPA Direct Debit Core First Return',
        '01218': 'SEPA Direct Debit Core Recurrent Return',
        '01219': 'SEPA Direct Debit Core Last Return',
        '01225': 'SEPA Direct Debit B2B Return',
        '01226': 'SEPA Direct Debit B2B One Off Return',
        '01227': 'SEPA Direct Debit B2B First Return',
        '01228': 'SEPA Direct Debit B2B Recurrent Return',
        '01229': 'SEPA Direct Debit B2B Last Return',
        '01301': 'SEPA Direct Debit Refund',
        '01302': 'SEPA Direct Debit One Off Refund',
        '01303': 'SEPA Direct Debit First Refund',
        '01304': 'SEPA Direct Debit Recurrent Refund',
        '01305': 'SEPA Direct Debit Last Refund',
        '01315': 'SEPA Direct Debit Core Refund',
        '01316': 'SEPA Direct Debit Core One Off Refund',
        '01317': 'SEPA Direct Debit Core First Refund',
        '01318': 'SEPA Direct Debit Core Recurrent Refund',
        '01319': 'SEPA Direct Debit Core Last Refund',
        '01401': 'SEPA Direct Debit Reversal',
        '01402': 'SEPA Direct Debit One Off Reversal',
        '01403': 'SEPA Direct Debit First Reversal',
        '01404': 'SEPA Direct Debit Recurrent Reversal',
        '01405': 'SEPA Direct Debit Last Reversal',
        '01415': 'SEPA Direct Debit Core Reversal',
        '01416': 'SEPA Direct Debit Core One Off Reversal',
        '01417': 'SEPA Direct Debit Core First Reversal',
        '01418': 'SEPA Direct Debit Core Recurrent Reversal',
        '01419': 'SEPA Direct Debit Core Last Reversal',
        '01425': 'SEPA Direct Debit B2BReversal',
        '01426': 'SEPA Direct Debit B2B One Off Reversal',
        '01427': 'SEPA Direct Debit B2B First Reversal',
        '01428': 'SEPA Direct Debit B2B Recurrent Reversal',
        '01429': 'SEPA Direct Debit B2B Last Reversal',
        '01501': 'SEPA Direct Debit Cancellation',
        '01502': 'SEPA Direct Debit One Off Cancellation',
        '01503': 'SEPA Direct Debit First Cancellation',
        '01504': 'SEPA Direct Debit Recurrent Cancellation',
        '01505': 'SEPA Direct Debit Last Cancellation',
        '01515': 'SEPA Direct Debit Core Cancellation',
        '01516': 'SEPA Direct Debit Core One Off Cancellation',
        '01517': 'SEPA Direct Debit Core First Cancellation',
        '01518': 'SEPA Direct Debit Core Recurrent Cancellation',
        '01519': 'SEPA Direct Debit Core Last Cancellation',
        '01525': 'SEPA Direct Debit B2BCancellation',
        '01526': 'SEPA Direct Debit B2B One Off Cancellation',
        '01527': 'SEPA Direct Debit B2B First Cancellation',
        '01528': 'SEPA Direct Debit B2B Recurrent Cancellation',
        '01529': 'SEPA Direct Debit B2B Last Cancellation',
        '02000': 'Point of Sale',
        '02010': 'Cross Border Point of Sale',
        '02100': 'Point of Sale Merchant',
        '02110': 'Foreign Currency Coins withdrawal counter',
        '02120': 'Sealbag deposit Foreign Currency bank notes',
        '02130': 'Returned POS DebitCard',
        '02500': 'Point of Sale abroad',
        '02510': 'FCY Mixed withdrawal counter',
        '02901': 'Dom POS Chipknip global',
        '02902': 'Dom ATM unload Chipknip (deposit)',
        '02990': 'Dom ATM load Chipknip',
        '02991': 'Reject Dom ATM load Chipknip',
        '02992': 'Reversal Dom POS payment Chipknip',
        '02993': 'Correction/repair Dom ATM unload Chipknip',
        '02994': 'Reversal Dom ATM unload Chipknip',
        '03000': 'ATM Withdrawal',
        '03010': 'ATM Withdrawal Foreign Currency',
        '03090': 'Correction Dom Cash withdrawal ATM',
        '03091': 'ATM Refund',
        '03100': 'Generic cash withdrawal ATM CreditCard',
        '03200': 'Cash Withdrawal',
        '03700': 'Cash deposit',
        '03804': 'Sealbag',
        '04000': 'Cheques',
        '04001': "Traveler's Cheques",
        '04002': 'Bank Cheques',
        '05000': 'Cash Balancing',
        '09000': 'Miscellaneous (ING)',
        '09001': 'Cost/Charges',
        '09002': 'Cost/Charges',
        '09003': 'Cost/Charges International Payment',
        '09004': 'Fee',
        '09101': 'Debit interest',
        '09102': 'Credit interest',
        '09800': 'Netting',
        '09801': 'Netting settlement reversal',
        '09900': 'Rectification',
        '09901': 'Rectification Value date',
        '09902': 'Rectification Cost/Charges',

        # legacy codes
        'SALA': 'Salary Payments',
        'INTC': 'Intracompany Payments',
        'TREA': 'Treasury Payments',
    }

    def code_is_valid(self, code):
        try:
            self.resolve_code(code)
            return True
        except InvalidIngTransactionCodeError:
            return False

    def resolve_code(self, code):
        try:
            return self.codes[code]
        except KeyError:
            raise InvalidIngTransactionCodeError("Code not found: %s" % code)


class SwiftTransactionCodes(AbstractTransactionCodes):
    '''These are SWIFT transaction codes.

    From the spec:
    De volgende SWIFT transactietypen worden gebruikt voor ING rekeningen.
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

        # Legacy codes (Legacy tag61 sub6)
        'NAC': 'Acceptgiro',
        'NBA': 'Cash dispenser transaction',
        'NCH': 'Cheque',
        'NDV': 'Sundry charges / miscellaneous',
        'NFL': 'Branch entry, intercompany entry',
        'NGF': 'Telephone transfer',
        'NGM': 'ATM',
        'NGT': 'Electronic transfer',
        'NIC': 'Credit of the total amount or debit of e.g. reversals',
        'NOV': 'Manual transfer',
        'NPK': 'Withdrawal',
        'NPO': 'Standing order',
        'NST': 'Deposit (own account or third-party)',
        'NVZ': 'Multi-transfer order (debit of the total amount or credit of the combined entries)',

        '001': 'transfer to current account',
        '002': 'transfer to private account',
        '003': 'transfer to deposit account',
        '004': 'transfer',
        '005': 'transfer to bank savings account',
        '024': 'interest on overdue payments',
        '026': 'electronic transfer',
        '027': 'transfer to foreign abroad',
        '028': 'closing entry to a suspense account',
        '029': 'Direct Debit or Multi-transfer order',
        '030': 'all cash payments charged to own customers',
        '031': 'settled receipts charged to own customers',
        '032': 'other branch payment, cheque received for collection',
        '033': 'purchase of securities',
        '034': 'coupons made payable',
        '035': 'transfer abroad',
        '036': 'transfer',
        '037': 'standing order',
        '038': 'collections',
        '039': 'one-off closure (interest)',
        '040': 'one-off closure (commission)',
        '041': 'one-off closure (charges)',
        '042': 'automatically entered (interest)',
        '043': 'automatically entered (commission)',
        '044': 'automatically entered (charges)',
        '045': 'urgent payment',
        '046': 'insurance premium invoices, etc.',
        '047': 'central payment scheme',
        '048': 'transfer (other)',
        '049': 'guaranteed cheque',
        '050': "travel money provided (traveller's cheques, foreign) currency)",
        '051': 'automatic transfer (quarterly closure)',
        '054': 'movements without turnover commission',
        '055': 'cash deposit',
        '056': 'sale of securities',
        '057': 'sales of coupons',
        '058': 'transfer abroad',
        '059': 'transfer bank',
        '060': 'salary credits',
        '061': 'transfer',
        '062': 'transfer',
        '063': 'settlement of collections',
        '064': 'one-off closure (interest)',
        '065': 'one-off closure (commission)',
        '066': 'one-off closure (charges)',
        '067': 'automatic interest entry',
        '068': 'insurance claims payments',
        '069': 'central processing',
        '070': 'transfer (others)',
        '071': 'settlement of guaranteed cheque',
        '072': "crediting of foreign currency purchased, traveller's cheques",
        '073': 'automatic transfer (quarterly closure)',
        '075': 'settlement of point of pay terminal',
        '076': 'settlement of chipknip (merchants)',
        '077': 'telephone transfer',
        '078': 'transfer',
        '079': 'transfer abroad',
        '080': 'one-off movements without turnover commission',
        '081': 'transfer from current account',
        '082': 'transfer from personal account',
        '083': 'transfer from deposit account',
        '084': 'transfer',
        '085': 'transfer from bank savings',
        '086': 'payments into night safe and credited to third parties',
        '087': 'electronic transfer',
    }

    def code_is_valid(self, code):
        try:
            self.resolve_code(code)
            return True
        except InvalidSwiftTransactionCodeError:
            return False

    def resolve_code(self, code):
        try:
            return self.codes[code]
        except KeyError:
            raise InvalidSwiftTransactionCodeError("Code not found: %s" % code)
