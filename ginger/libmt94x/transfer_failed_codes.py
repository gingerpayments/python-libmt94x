class InvalidTransferFailedCodeError(Exception):
    pass


class AbstractTransferFailed(object):
    '''Abstract class for all transfer failed classes.'''

    # Populate this in derived classes
    codes = {}
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
        except InvalidTransferFailedCodeError:
            return False

    def resolve_code(self, code):
        try:
            return self.codes[code]
        except KeyError:
            raise InvalidTransferFailedCodeError("Code not found: %s" % code)


class TransferFailedSEPA(AbstractTransferFailed):
    '''NL term: redenen niet-boeking SEPA

    De ISO-redenen van niet boeking in de onderstaande tabel zijn van
    toepassing op de SEPA overboeking en/of de SEPA incasso.'''

    # iso code -> description
    codes = {
        'AC01': 'Rekeningnummer incorrect',
        'AC04': 'Rekeningnummer gesloten',
        'AC06': 'Rekeningnummer geblokkeerd',
        'AC13': 'Debiteur rekening is ongeldig',
        'AG01': 'Transactie niet toegestaan',
        'AG02': 'Ongeldig bank operatie code',
        'AM04': 'Onvoldoende saldo',
        'AM05': 'Dubbel betaald',
        'BE01': 'Debiteur naam en rekening komen niet overeen',
        'BE04': 'Adres crediteur ontbreekt of incorrect',
        'BE05': 'Identificatie van de crediteur is incorrect',
        'CNOR': 'Bank van de crediteur is onbekend onder deze BIC',
        'DNOR': 'Bank van de debiteur is onbekend onder deze BIC',
        'FF01': 'Transactiecode of bestandsformaat incorrect',
        'FF05': 'Incasso type incorrect',
        'FOCR': 'Terugboeking na annuleringsverzoek',
        'MD01': 'Geen machtiging verstrekt',
        'MD02': 'Verplichte informatie over machtiging ontbreekt of incorrect',
        'MD06': 'Terugboeking op verzoek van klant',
        'MD07': 'Klant overleden',
        'MS02': 'Onbekende reden klant',
        'MS03': 'Onbekende reden bank',
        'RC01': 'BIC incorrect',
        'RR01': 'Wet of regelgeving',
        'RR02': 'Voor wet of regelgeving benodigde naam/enof adres van de debiteur is onvolledig of ontbreekt.',
        'RR03': 'Voor wet of regelgeving benodigde naam/enof adres van de crediteur ontbreekt.',
        'RR04': 'Wet of regelgeving',
        'SL01': 'Specifieke dienstverlening bank (bv selectieve incassoblokkade)',
        'TM01': 'Bestand aangeleverd na cut-off tijd (uiterste aanlevertijdstip)',
    }


class TransferFailedMisc(AbstractTransferFailed):
    '''NL term: redenen niet-boeking overig

    De ISO-redenen van niet-boeking in de onderstaande tabel zijn generieke
    codes en kunnen van toepassing zijn op alle betalingen ook op
    SEPA-transacties'''

    # iso code -> description
    codes = {
        'AC03': 'Ongeldig rekeningnummer crediteur',
        'AGNT': 'Onjuiste agent',
        'AM01': 'Bedrag van de transactie is nul',
        'AM02': 'Bedrag niet toegestaan-contract',
        'AM06': 'Bedrag te laag-contract',
        'AM07': 'Geblokkeerd bedrag',
        'AM09': 'Onjuist bedrag-contract',
        'AM10': 'Ongeldig controle getal',
        'ARDT': 'Transactie al terugbetaald',
        'BE06': 'Indentificatie crediteur onbekend',
        'CURR': 'Onjuiste valuta',
        'CUST': 'Terugboeking gevraagd debiteur',
        'CUTA': 'Opdracht teruggeboekt definitief',
        'DT01': 'Ongeldige datum',
        'ED01': 'Correspondent bank is onjuist',
        'ED03': 'Verzoek voor saldo informatie',
        'ED05': 'Settlement niet uitgevoerd',
        'EMVL': 'Wet/regelgeing Card transactie (PIN)',
        'MD04': 'Ongeldig bestandsformaat',
        'MD05': 'Ongeldig incasso crediteur of agent',
        'NARR': 'Reden afschrijving meegegeven',
        'NOAS': 'Geen antwoord van de klant',
        'NOOR': 'Geen transactie ontvangen',
        'PINL': 'Wet/regelgeing Card transactie (PIN)',
        'PY01': 'Correspondent bank onjuist',
        'RC07': 'BIC incorrect van crediteur',
        'RF01': 'Transactie referentie niet uniek',
        'SL02': 'Specifieke dienstverlening agent van crediteur',
        'SVNR': 'Card betaling niet uitgevoerd',
        'TECH': 'Onjuiste incasso (technisch probleem)',
        'XT78': 'Controle op saldo niet gelukt',
        'XT79': 'Debiteur agent niet gemachtigd',
        'XT80': 'Crediteur agent niet gemachtigd',
        'XT87': 'Terugboeking volgt andere weg',
    }


class TransferFailed(AbstractTransferFailed):
    '''Convenience class that collects all possible transfer failed codes and
    provides a matching API.'''

    def __init__(self):
        self.sepa = TransferFailedSEPA.get_instance()
        self.misc = TransferFailedMisc.get_instance()

    def code_is_valid(self, code):
        return self.sepa.code_is_valid(code) or self.misc.code_is_valid(code)

    def resolve_code(self, code):
        try:
            return self.sepa.resolve_code(code)
        except InvalidTransferFailedCodeError:
            return self.misc.resolve_code(code)
