import pycountry


class InvalidCurrencyCodeError(Exception):
    pass


class CurrencyCodes(object):
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
        except InvalidCurrencyCodeError:
            return False

    def resolve_code(self, code):
        try:
            currency = pycountry.currencies.get(letter=code)
            return currency.name
        except KeyError:
            raise InvalidCurrencyCodeError("Code not found: %s" % code)
