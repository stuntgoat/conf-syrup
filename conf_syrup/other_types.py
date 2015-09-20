import logging

from conf_syrup.exceptions import IOErrorWhileReading

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('conf_syrup.other_types')


def LogLEVEL(val):
    """
    Return a sane loglevel given some value.

    """
    if isinstance(val, (float, int)):
        return int(val)
    if isinstance(val, basestring):
        return getattr(logging, val.upper())
    return val


def ValFromFile(val, throw=True):
    """
    Read the contents from a file.

    Usually, this will be a single value on the first line.

    If `throw`, we raise a FileNotFound
    """
    try:
        f = open(val, 'r')
    except IOError as e:
        LOGGER.error(str(e))
        if throw:
            raise IOErrorWhileReading(str(e))
        LOGGER.info('unable to open %s for reading; returning an empty string')
        return ''
    return f.read().strip()


def SafeValFromFile(val):
    return ValFromFile(val, throw=False)
