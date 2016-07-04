from libmt94x.info_acct_owner_subfields import BeneficiaryParty
from libmt94x.info_acct_owner_subfields import BusinessPurpose
from libmt94x.info_acct_owner_subfields import Charges
from libmt94x.info_acct_owner_subfields import ClientReference
from libmt94x.info_acct_owner_subfields import CounterPartyID
from libmt94x.info_acct_owner_subfields import CounterPartyIdentification
from libmt94x.info_acct_owner_subfields import CreditorID
from libmt94x.info_acct_owner_subfields import EndToEndReference
from libmt94x.info_acct_owner_subfields import ExchangeRate
from libmt94x.info_acct_owner_subfields import InstructionID
from libmt94x.info_acct_owner_subfields import InfoToAcccountOwnerSubFieldOrder
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
from libmt94x.textutil import break_at_width
from libmt94x.textutil import format_amount


class Mt94xWriter(object):
    def __init__(self, serializer):
        self.serializer = serializer

    def _write_code_word(self, serializer, code_word):
        serializer.chars(5, b'/%s' % code_word.tag)

        if isinstance(code_word, BeneficiaryParty):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.account_number if code_word.account_number else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(11, code_word.bic if code_word.bic else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(50, code_word.name if code_word.name else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.city if code_word.city else '')

        elif isinstance(code_word, BusinessPurpose):
            serializer.chars(1, b'/')
            serializer.chars_noslash(24, code_word.id_code if code_word.id_code else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(9, (code_word.sepa_transaction_type if
                                         code_word.sepa_transaction_type else ''))

        elif isinstance(code_word, Charges):
            serializer.chars(1, b'/')
            serializer.chars_noslash(15, code_word.charges)

        elif isinstance(code_word, ClientReference):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.client_reference)

        elif isinstance(code_word, CounterPartyID):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.account_number if code_word.account_number else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(11, code_word.bic if code_word.bic else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(50, code_word.name if code_word.name else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.city if code_word.city else '')

        elif isinstance(code_word, CounterPartyIdentification):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.id_code if code_word.id_code else '')

        elif isinstance(code_word, CreditorID):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.creditor_id if code_word.creditor_id else '')

        elif isinstance(code_word, EndToEndReference):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, (code_word.end_to_end_reference
                                          if code_word.end_to_end_reference else ''))

        elif isinstance(code_word, ExchangeRate):
            serializer.chars(1, b'/')
            serializer.chars_noslash(12, code_word.exchange_rate)

        elif isinstance(code_word, InstructionID):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.instruction_id)

        elif isinstance(code_word, MandateReference):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.mandate_reference)

        elif isinstance(code_word, OrderingParty):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.account_number if code_word.account_number else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(11, code_word.bic if code_word.bic else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(50, code_word.name if code_word.name else '')

            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.city if code_word.city else '')

        elif isinstance(code_word, PaymentInformationID):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.payment_information_id)

        elif isinstance(code_word, PurposeCode):
            serializer.chars(1, b'/')
            serializer.chars_noslash(4, code_word.purpose_of_collection)

        elif isinstance(code_word, RemittanceInformation):
            # We allow slashes in this subfield
            if isinstance(code_word.remittance_info, UnstructuredRemittanceInfo):
                serializer.chars(255, b'/USTD//%s'
                                 % code_word.remittance_info.remittance_info)

            elif isinstance(code_word.remittance_info, DutchStructuredRemittanceInfo):
                serializer.chars(255, b'/STRD/CUR/%s'
                                 % code_word.remittance_info.payment_reference)

            elif isinstance(code_word.remittance_info, IsoStructuredRemittanceInfo):
                serializer.chars(255, b'/STRD/ISO/%s'
                                 % code_word.remittance_info.iso_reference)

        elif isinstance(code_word, ReturnReason):
            serializer.chars(1, b'/')
            serializer.chars_noslash(4, code_word.reason_code)

        elif isinstance(code_word, UltimateBeneficiary):
            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.name)

        elif isinstance(code_word, UltimateCreditor):
            serializer.chars(1, b'/')
            serializer.chars(70, code_word.name if code_word.name else '')  # allow slash

            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.id if code_word.id else '')

        elif isinstance(code_word, UltimateDebtor):
            serializer.chars(1, b'/')
            serializer.chars(70, code_word.name if code_word.name else '')  # allow slash

            serializer.chars(1, b'/')
            serializer.chars_noslash(35, code_word.id if code_word.id else '')

        serializer.chars(1, b'/')

    # Fields

    def write_account_identification(self, ai):
        record = (self.serializer
            .start()
            .chars(4, b':%s:' % ai.tag)
            .chars(35, b'%s%s' % (ai.iban, (ai.iso_currency_code if
                                            ai.iso_currency_code else '')))
            .newline()
            .finish()
        )
        return record

    def write_closing_available_balance(self, cab):
        record = (self.serializer
            .start()
            .chars(4, b':%s:' % cab.tag)
            .chars(1, b'C' if cab.type == cab.TYPE_CREDIT else b'D')
            .date_yymmdd(cab.date)
            .chars(3, cab.currency)
            .amount(15, cab.currency, cab.amount)
            .newline()
            .finish()
        )
        return record

    def write_closing_balance(self, cb):
        record = (self.serializer
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
        record = (self.serializer
            .start()
            .chars(4, b':%s:' % fab.tag)
            .chars(1, b'C' if fab.type == fab.TYPE_CREDIT else b'D')
            .date_yymmdd(fab.date)
            .chars(3, fab.currency)
            .amount(15, fab.currency, fab.amount)
            .newline()
            .finish()
        )
        return record

    def write_information_to_account_owner_ibp(self, info):
        maxlen = 6 * 65

        # Write out the tag
        (self.serializer
            .start())

        # Write out all the subfields (order is undefined)
        for code_word in info.code_words:
            self._write_code_word(self.serializer, code_word)

        # Write out the free form text (note that this excludes subfields above)
        if info.free_form_text:
            self.serializer.chars(maxlen, info.free_form_text)

        # Terminate the value
        info_part = (self.serializer
            .newline()
            .finish())

        # Check max length (note that this applies to the info part only, not
        # the whole record)
        if len(info_part) > maxlen:
            raise ValueError("Record exceeds maximum length: %s" % maxlen)

        # Break lines at character 65
        info_part = break_at_width(info_part, width=65, newline='\r\n')

        # Write out the tag
        tag_part = (self.serializer
            .start()
            .chars(5, b':%s:' % info.tag)
            .finish())

        # Concat tag and info part
        record = b'%s%s' % (tag_part, info_part)

        return record

    def write_information_to_account_owner_ming(self, info):
        maxlen = 6 * 65

        # Write out the tag
        (self.serializer
            .start()
            .chars(5, b':%s:' % info.tag))

        # Write out all the subfields (order is defined)
        for code_word_cls in InfoToAcccountOwnerSubFieldOrder.get_field_classes():
            code_word = info.get_code_word_by_cls(code_word_cls)
            if code_word is not None:
                self._write_code_word(self.serializer, code_word)

        # Terminate the record
        record = (self.serializer
            .newline()
            .finish())

        # Check max length
        if len(record) > maxlen:
            raise ValueError("Record exceeds maximum length: %s" % maxlen)

        # Break lines at character 65
        record = break_at_width(record, width=65, newline='\r\n')

        return record

    def write_information_to_account_owner_totals_ibp(self, info):
        record = (self.serializer
            .start()
            .chars(5, b':%s:' % info.tag)
            .chars(1, b'D')
            .num(6, b'%s' % info.num_debit, leading_zero=True)
            .chars(1, b'C')
            .num(6, b'%s' % info.num_credit, leading_zero=True)
            .chars(1, b'D')
            .amount(15, None, info.amount_debit)
            .chars(1, b'C')
            .amount(15, None, info.amount_credit)
            .newline()
            .finish()
        )
        return record

    def write_information_to_account_owner_totals_ming(self, info):
        record = (self.serializer
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
        record = (self.serializer
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
        supplementary_details = b''
        if sl.ing_transaction_code:
            supplementary_details = b'/TRCD/%s/' % sl.ing_transaction_code
            if sl.original_amount_of_transaction:
                amount = format_amount(sl.original_amount_of_transaction.amount,
                                       self.serializer.locale)
                supplementary_details = b'%s/OCMT/%s%s/' % (
                    supplementary_details,
                    sl.original_amount_of_transaction.currency,
                    amount,
                )

        record = (self.serializer
            .start()
            .chars(4, b':%s:' % sl.tag)
            .date_yymmdd(sl.value_date)
            .chars(1, b'C' if sl.type == sl.TYPE_CREDIT else b'D')
            .amount(15, None, sl.amount)
            .chars(4, b'N%s' % sl.transaction_code)
            .chars_noslash(16, sl.reference_for_account_owner or b'NONREF')
            .chars_noslash(16, (sl.account_servicing_institutions_reference
                                if sl.account_servicing_institutions_reference else ''))
            # Supplementary Details
            .chars(34, supplementary_details)
            .newline()
            .finish()
        )
        return record

    def write_statement_line_ming(self, sl):
        record = (self.serializer
            .start()
            .chars(4, b':%s:' % sl.tag)
            .date_yymmdd(sl.value_date)
            .date_mmdd(sl.book_date)
            .chars(1, b'C' if sl.type == sl.TYPE_CREDIT else b'D')
            .amount(15, None, sl.amount)
            .chars(4, b'N%s' % sl.transaction_code)
            .chars_noslash(16, sl.reference_for_account_owner or b'NONREF')
            .chars(2, b'//').chars_noslash(14, sl.transaction_reference)
            .newline()
            .chars(34, b'/TRCD/%s/' % sl.ing_transaction_code)
            .newline()
            .finish()
        )
        return record

    def write_statement_number(self, sn):
        record = (self.serializer
            .start()
            .chars(5, b':%s:' % sn.tag)
            .num(5, sn.statement_number)
            .newline()
            .finish()
        )
        return record

    def write_transaction_reference_number_ibp(self, trn):
        record = (self.serializer
            .start()
            .chars(4, b':%s:' % trn.tag)
            .chars(16, b'ING')
            .newline()
            .finish()
        )
        return record

    def write_transaction_reference_number_ming(self, trn):
        record = (self.serializer
            .start()
            .chars(4, b':%s:' % trn.tag)
            .chars(16, trn.transaction_reference_number)
            .newline()
            .finish()
        )
        return record

    # Prolog and Epilog

    def write_message_information_ibp(self):
        block = (self.serializer
            .start()
            .chars(6, b'940 00')
            .newline()
            .finish())
        return block

    def write_prolog_ming(self):
        block = (self.serializer
            .start()
            .chars(3, b'{4:')
            .newline()
            .finish())
        return block

    def write_epilog_ibp(self):
        block = (self.serializer
            .start()
            .chars(4, b'-XXX')
            .finish())
        return block

    def write_epilog_ming(self):
        block = (self.serializer
            .start()
            .chars(2, b'-}')
            .finish())
        return block

    def write_export_info_ibp(self, info):
        # Some of these values are constants
        block = (self.serializer
            .start()
            .chars(4, b'0000')
            .chars(1, b' ')
            .chars(2, b'01')
            .chars(12, info.export_address)
            .chars(5, info.export_number)
            .newline()
            .finish())
        return block

    def write_export_info_ming(self):
        # NOTE: This appears to be a constant value
        block = (self.serializer
            .start()
            .chars(29, b'{1:F01INGBNL2ABXXX0000000000}')
            .newline()
            .finish())
        return block

    def write_import_info_ibp(self, info):
        # Some of these values are constants
        block = (self.serializer
            .start()
            .chars(4, b'0000')
            .chars(1, b' ')
            .chars(2, b'01')
            .chars(12, info.import_address)
            .chars(5, info.import_number)
            .newline()
            .finish())
        return block

    def write_import_info_ming(self):
        # NOTE: This appears to be a constant value
        block = (self.serializer
            .start()
            .chars(20, b'{2:I940INGBNL2AXXXN}')
            .newline()
            .finish())
        return block

    # Document

    def write_document_ibp(self, doc):
        blocks = []

        # export info
        if doc.export_info is None:
            raise ValueError("Document missing export_info")

        export = self.write_export_info_ibp(doc.export_info)
        blocks.append(export)

        # import info
        if doc.import_info is None:
            raise ValueError("Document missing import_info")

        import_ = self.write_import_info_ibp(doc.import_info)
        blocks.append(import_)

        # 940 00
        prolog = self.write_message_information_ibp()
        blocks.append(prolog)

        # :20:
        trn = self.write_transaction_reference_number_ibp(
            doc.transaction_reference_number)
        blocks.append(trn)

        # :25:
        ai = self.write_account_identification(doc.account_identification)
        blocks.append(ai)

        # :28C:
        sn = self.write_statement_number(doc.statement_number)
        blocks.append(sn)

        # :60F:
        ob = self.write_opening_balance(doc.opening_balance)
        blocks.append(ob)

        # entries: :61: & :86:
        for statement_line, infos in doc.entries.items():
            sl = self.write_statement_line_ibp(statement_line)
            blocks.append(sl)
            for info in infos:
                inf = self.write_information_to_account_owner_ibp(info)
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
        info_tot = self.write_information_to_account_owner_totals_ibp(
            doc.info_to_acct_owner_totals)
        blocks.append(info_tot)

        # -XXX
        epilog = self.write_epilog_ibp()
        blocks.append(epilog)

        block = ''.join(blocks)
        return block

    def write_document_ming(self, doc):
        blocks = []

        # {1:...}
        export = self.write_export_info_ming()
        blocks.append(export)

        # {2:...}
        import_ = self.write_import_info_ming()
        blocks.append(import_)

        # {4:
        prolog = self.write_prolog_ming()
        blocks.append(prolog)

        # :20:
        trn = self.write_transaction_reference_number_ming(
            doc.transaction_reference_number)
        blocks.append(trn)

        # :25:
        ai = self.write_account_identification(doc.account_identification)
        blocks.append(ai)

        # :28C:
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
