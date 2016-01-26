from ginger.libmt94x.info_acct_owner_subfields import CounterPartyID
from ginger.libmt94x.info_acct_owner_subfields import CreditorID
from ginger.libmt94x.info_acct_owner_subfields import EndToEndReference
from ginger.libmt94x.info_acct_owner_subfields import InfoToAcccountOwnerSubFieldOrder
from ginger.libmt94x.info_acct_owner_subfields import MandateReference
from ginger.libmt94x.info_acct_owner_subfields import PaymentInformationID
from ginger.libmt94x.info_acct_owner_subfields import PurposeCode
from ginger.libmt94x.info_acct_owner_subfields import RemittanceInformation
from ginger.libmt94x.info_acct_owner_subfields import ReturnReason
from ginger.libmt94x.info_acct_owner_subfields import UltimateCreditor
from ginger.libmt94x.info_acct_owner_subfields import UltimateDebtor
from ginger.libmt94x.remittance_info import DutchStructuredRemittanceInfo
from ginger.libmt94x.remittance_info import IsoStructuredRemittanceInfo
from ginger.libmt94x.remittance_info import UnstructuredRemittanceInfo
from ginger.libmt94x.textutil import break_at_width


class Tm94xWriter(object):
    def __init__(self, serializer):
        self.ser = serializer


    def _write_code_word(self, serializer, code_word):
        serializer.chars(5, b'/%s' % code_word.tag)

        if isinstance(code_word, ReturnReason):
            serializer.chars(5, b'/%s' % code_word.reason_code)
        elif isinstance(code_word, EndToEndReference):
            serializer.chars(35, b'/%s' % code_word.end_to_end_reference)
        elif isinstance(code_word, PaymentInformationID):
            serializer.chars(35, b'/%s' % code_word.payment_information_id)
        elif isinstance(code_word, MandateReference):
            serializer.chars(35, b'/%s' % code_word.mandate_reference)
        elif isinstance(code_word, CreditorID):
            serializer.chars(35, b'/%s' % code_word.creditor_id)
        elif isinstance(code_word, CounterPartyID):
            serializer.chars(36, b'/%s' % (code_word.account_number if code_word.account_number else ''))
            serializer.chars(12, b'/%s' % (code_word.bic if code_word.bic else ''))
            serializer.chars(51, b'/%s' % (code_word.name if code_word.name else ''))
            serializer.chars(36, b'/%s' % (code_word.city if code_word.city else ''))
        elif isinstance(code_word, RemittanceInformation):
            if isinstance(code_word.remittance_info, UnstructuredRemittanceInfo):
                serializer.chars(256, b'/USTD//%s'
                                 % code_word.remittance_info.remittance_info)
            if isinstance(code_word.remittance_info, DutchStructuredRemittanceInfo):
                serializer.chars(256, b'/STRD/CUR/%s'
                                 % code_word.remittance_info.payment_reference)
            if isinstance(code_word.remittance_info, IsoStructuredRemittanceInfo):
                serializer.chars(256, b'/STRD/ISO/%s'
                                 % code_word.remittance_info.iso_reference)
        elif isinstance(code_word, PurposeCode):
            serializer.chars(5, b'/%s' % code_word.purpose_of_collection)
        elif isinstance(code_word, UltimateCreditor):
            serializer.chars(71, b'/%s' % (code_word.name if code_word.name else ''))
            serializer.chars(36, b'/%s' % (code_word.id if code_word.id else ''))
        elif isinstance(code_word, UltimateDebtor):
            serializer.chars(71, b'/%s' % (code_word.name if code_word.name else ''))
            serializer.chars(36, b'/%s' % (code_word.id if code_word.id else ''))

        serializer.chars(1, b'/')

    # Fields

    def write_account_identification(self, ai):
        record = (self.ser
            .start()
            .chars(4, b':%s:' % ai.tag)
            .chars(35, b'%s%s' % (ai.iban, ai.iso_currency_code))
            .newline()
            .finish()
        )
        return record

    def write_closing_available_balance(self, cab):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % cab.tag)
            .chars(1, b'C' if cab.type == cab.TYPE_CREDIT else b'D')
            .date_yymmdd(cab.date)
            .chars(3, cab.currency)
            .amount(15, cab.currency, cab.amount)
            .newline()
            .finish()
        )
        return record

    def write_closing_balance(self, cb):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % cb.tag)
            .chars(1, b'C' if cb.type == cb.TYPE_CREDIT else b'D')
            .date_yymmdd(cb.date)
            .chars(3, cb.currency)
            .amount(15, cb.currency, cb.amount)
            .newline()
            .finish()
        )
        return record

    def write_forward_available_balance(self, fab):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % fab.tag)
            .chars(1, b'C' if fab.type == fab.TYPE_CREDIT else b'D')
            .date_yymmdd(fab.date)
            .chars(3, fab.currency)
            .amount(15, fab.currency, fab.amount)
            .newline()
            .finish()
        )
        return record

    def write_information_to_account_owner_totals_ibp(self, info):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % info.tag)
            .chars(1, b'D')
            .num(6, b'%s' % info.num_debit)
            .chars(1, b'C')
            .num(6, b'%s' % info.num_credit)
            .chars(1, b'D')
            .amount(15, None, info.amount_debit)
            .chars(1, b'C')
            .amount(15, None, info.amount_credit)
            .newline()
            .finish()
        )
        return record

    def write_information_to_account_owner_ming(self, info):
        # Write out the tag
        (self.ser
            .start()
            .chars(5, b':%s:' % info.tag))

        # Write out all the subfields
        for code_word_cls in InfoToAcccountOwnerSubFieldOrder.get_field_classes():
            code_word = info.get_code_word_by_cls(code_word_cls)
            if code_word is not None:
                self._write_code_word(self.ser, code_word)

        # Terminate the record
        record = (self.ser
            .newline()
            .finish())

        # Check max length
        maxlen = 6 * 65
        if len(record) > maxlen:
            raise ValueError("Record exceeds maximum length: %s" % maxlen)

        # Break lines at character 65
        record = break_at_width(record, width=65, newline='\r\n')

        return record

    def write_information_to_account_owner_totals_ming(self, info):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % info.tag)
            .chars(5, b'/SUM/')
            .num(6, b'%s' % info.num_debit)
            .chars(1, b'/')
            .num(6, b'%s' % info.num_credit)
            .chars(1, b'/')
            .amount(15, None, info.amount_debit)
            .chars(1, b'/')
            .amount(15, None, info.amount_credit)
            .chars(1, b'/')
            .newline()
            .finish()
        )
        return record

    def write_opening_balance(self, ob):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % ob.tag)
            .chars(1, b'C' if ob.type == ob.TYPE_CREDIT else b'D')
            .date_yymmdd(ob.date)
            .chars(3, ob.currency)
            .amount(15, ob.currency, ob.amount)
            .newline()
            .finish()
        )
        return record

    def write_statement_line_ibp(self, sl):
        record = (self.ser
            .start()
            .chars(4, b':%s:' % sl.tag)
            .date_yymmdd(sl.value_date)
            .chars(1, b'C' if sl.type == sl.TYPE_CREDIT else b'D')
            .amount(15, None, sl.amount)
            .chars(4, b'N%s' % sl.transaction_code)
            .chars(16, sl.reference_for_account_owner or b'NONREF')
            .chars(16, sl.account_servicing_institutions_reference)  # FIXME: optional
            # Supplementary Details
            .chars(34, b'/TRCD/%s/' % sl.ing_transaction_code)
            # FIXME: /OCMT/USD1234,50/
            .newline()
            .finish()
        )
        return record

    def write_statement_line_ming(self, sl):
        record = (self.ser
            .start()
            .chars(4, b':%s:' % sl.tag)
            .date_yymmdd(sl.value_date)
            .date_mmdd(sl.book_date)
            .chars(1, b'C' if sl.type == sl.TYPE_CREDIT else b'D')
            .amount(15, None, sl.amount)
            .chars(4, b'N%s' % sl.transaction_code)
            .chars(16, sl.reference_for_account_owner or b'NONREF')
            .chars(16, b'//%s' % sl.transaction_reference)
            .newline()
            .chars(34, b'/TRCD/%s/' % sl.ing_transaction_code)
            .newline()
            .finish()
        )
        return record

    def write_statement_number(self, sn):
        record = (self.ser
            .start()
            .chars(5, b':%s:' % sn.tag)
            .num(5, sn.statement_number)
            .newline()
            .finish()
        )
        return record

    def write_transaction_reference_number(self, trn):
        record = (self.ser
            .start()
            .chars(4, b':%s:' % trn.tag)
            .chars(16, trn.transaction_reference_number)
            .newline()
            .finish()
        )
        return record

    # Prolog and Epilog

    def write_prolog_ming(self):
        block = (self.ser
            .start()
            .chars(3, b'{4:')
            .newline()
            .finish())
        return block

    def write_epilog_ming(self):
        block = (self.ser
            .start()
            .chars(2, b'-}')
            .finish())
        return block

    # Document

    def write_document_ming(self, doc):
        blocks = []

        # {4:
        prolog = self.write_prolog_ming()
        blocks.append(prolog)

        # :20:
        trn = self.write_transaction_reference_number(
            doc.transaction_reference_number)
        blocks.append(trn)

        # :25:
        ai = self.write_account_identification(doc.account_identification)
        blocks.append(ai)

        # :28:
        sn = self.write_statement_number(doc.statement_number)
        blocks.append(sn)

        # :60F:
        ob = self.write_opening_balance(doc.opening_balance)
        blocks.append(ob)

        # entries: :61: & :86:
        for statement_line, infos in doc.entries.items():
            sl = self.write_statement_line_ming(statement_line)
            blocks.append(sl)
            for info in infos:
                inf = self.write_information_to_account_owner_ming(info)
                blocks.append(inf)

        # :62F:
        cb = self.write_closing_balance(doc.closing_balance)
        blocks.append(cb)

        # :64:
        cab = self.write_closing_available_balance(doc.closing_available_balance)
        blocks.append(cab)

        # :65:
        for forward_available_balance in doc.forward_available_balances:
            fab = self.write_forward_available_balance(forward_available_balance)
            blocks.append(fab)

        # :86:
        info_tot = self.write_information_to_account_owner_totals_ming(
            doc.info_to_acct_owner_totals)
        blocks.append(info_tot)

        # -}
        epilog = self.write_epilog_ming()
        blocks.append(epilog)

        block = ''.join(blocks)
        return block
