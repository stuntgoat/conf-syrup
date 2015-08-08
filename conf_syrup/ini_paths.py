import logging
from ConfigParser import ConfigParser
from os.path import abspath

from conf_syrup.bool_type import Bool
from conf_syrup.network_type import NetworkFromPrefix

CONF_PARSERS = {}

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger('conf_syrup.ini_paths')


def _get_cp(path):
    global CONF_PARSERS

    p = abspath(path)
    if p not in CONF_PARSERS:
        cp = ConfigParser()
        try:
            cp.read(p)
        except Exception as e:
            LOGGER.exception(e)
            raise

        CONF_PARSERS[p] = cp
    return CONF_PARSERS[p]


class INI_SectionKey(object):
    def __init__(self, path):
        self.path = abspath(path)

    def value_for_section_key(self, section):
        def f(val):
            _configparser = _get_cp(self.path)
            return _configparser.get(section, val)
        return f

    def MkInt(self, section):
        return lambda x: int(self.value_for_section_key(section)(x))

    def MkString(self, section):
        return lambda x: self.value_for_section_key(section)(x)

    def MkNetworkPrefix(self, section):
        return lambda x: NetworkFromPrefix(self.value_for_section_key(section)(x))

    def MkBool(self, section):
        return lambda x: Bool(self.value_for_section_key(section)(x))
