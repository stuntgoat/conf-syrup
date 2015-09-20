
class ConfSyrupException(Exception):
    pass


class InvalidOption(ConfSyrupException):
    pass


class UnableToLoadSettings(ConfSyrupException):
    pass


class ConflictingTypes(ConfSyrupException):
    pass


class IOErrorWhileReading(ConfSyrupException):
    pass
