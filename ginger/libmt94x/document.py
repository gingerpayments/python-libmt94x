from collections import OrderedDict

from ginger.libmt94x.fields import AccountIdentification
from ginger.libmt94x.fields import ClosingAvailableBalance
from ginger.libmt94x.fields import ClosingBalance
from ginger.libmt94x.fields import ForwardAvailableBalance
from ginger.libmt94x.fields import InformationToAccountOwnerTotals
from ginger.libmt94x.fields import OpeningBalance
from ginger.libmt94x.fields import StatementNumber
from ginger.libmt94x.fields import TransactionReferenceNumber


class Tm940Document(object):
    def __init__(self,
                 transaction_reference_number=None,
                 account_identification=None,
                 statement_number=None,
                 opening_balance=None,
                 entries=None,
                 closing_balance=None,
                 closing_available_balance=None,
                 forward_available_balances=None,
                 info_to_acct_owner_totals=None):

        # entries: { statement_line -> [ info_to_acct_owner] }
        entries = entries or []
        forward_available_balances = forward_available_balances or []

        if not isinstance(transaction_reference_number, TransactionReferenceNumber):
            raise ValueError(
                "Value `transaction_reference_number` must be "
                "an instance of TransactionReferenceNumber")

        if not isinstance(account_identification, AccountIdentification):
            raise ValueError(
                "Value `account_identification` must be "
                "an instance of AccountIdentification")

        if not isinstance(statement_number, StatementNumber):
            raise ValueError(
                "Value `statement_number` must be "
                "an instance of StatementNumber")

        if not isinstance(opening_balance, OpeningBalance):
            raise ValueError(
                "Value `opening_balance` must be "
                "an instance of OpeningBalance")

        # NOTE: We say OrderedDict, not just dict, otherwise the order of the
        # entries in the document is undefined
        if not isinstance(entries, OrderedDict):
            raise ValueError(
                "Value `entries` must be "
                "an OrderedDict whose values are lists")
        # Here we just probe the first value
        # We could make this less strict and just require that it be an iterable
        if not isinstance(entries.values()[0], list):
            raise ValueError(
                "Value `entries` must be "
                "an OrderedDict whose values are lists")

        if not isinstance(closing_balance, ClosingBalance):
            raise ValueError(
                "Value `closing_balance` must be "
                "an instance of ClosingBalance")

        if not isinstance(closing_available_balance, ClosingAvailableBalance):
            raise ValueError(
                "Value `closing_available_balance` must be "
                "an instance of ClosingAvailableBalance")

        for forward_available_balance in forward_available_balances:
            if not isinstance(forward_available_balance, ForwardAvailableBalance):
                raise ValueError(
                    "Value `forward_available_balance` must be "
                    "an instance of ForwardAvailableBalance")

        if not isinstance(info_to_acct_owner_totals, InformationToAccountOwnerTotals):
            raise ValueError(
                "Value `info_to_acct_owner_totals` must be "
                "an instance of InformationToAccountOwnerTotals")

        self.transaction_reference_number = transaction_reference_number
        self.account_identification = account_identification
        self.statement_number = statement_number
        self.opening_balance = opening_balance
        self.entries = entries
        self.closing_balance = closing_balance
        self.closing_available_balance = closing_available_balance
        self.forward_available_balances = forward_available_balances
        self.info_to_acct_owner_totals = info_to_acct_owner_totals
