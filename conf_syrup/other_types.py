import logging


def LogLEVEL(val):
    """
    Return a sane loglevel given some value.

    """
    if isinstance(val, (float, int)):
        return int(val)
    if isinstance(val, basestring):
        return getattr(logging, val.upper())
    return val


def ValFromFile(val):
    """
    Read a single value from a file.

    """
    f = open(val, 'r')
    return f.read().strip()
