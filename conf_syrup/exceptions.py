
class ConfSyrupException(Exception):
    pass


class InvalidOption(ConfSyrupException):
    pass


class UnableToLoadSettings(ConfSyrupException):
    pass
