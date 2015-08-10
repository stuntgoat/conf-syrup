import logging
import os

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('conf_syrup.settings')

from conf_syrup.exceptions import (
    InvalidOption,
    UnableToLoadSettings,
)


class Settings(object):
    def __init__(self, *confs):
        """
        `*confs` is one or more dictionary to be loaded in the order in which
        they are passed in.

        """
        self._raw = {}
        for conf in confs:
            self._raw.update(conf)

        self._data = {}
        self._env = os.environ

        self.load_settings()

    def __getattr__(self, attr):
        if attr in self._data:
            return self._data[attr]

        raise InvalidOption('%s not declared since calling load_settings!' % attr)

    def _load_key(self, k, data):
        in_env = k in self._env
        if isinstance(data, (tuple, list)):
            _type, _value = data

            if in_env:
                self._data[k] = _type(self._env[k])
            else:
                self._data[k] = _type(_value)
            return

        if in_env:
            self._data[k] = self._env[k]
        else:
            self._data[k] = data

    def load_settings(self):
        for k, data in self._raw.iteritems():
            try:
                self._load_key(k, data)
            except Exception as e:
                args = (k, data, e)
                msg = 'Unable to load value for key: %s with data: %s Error: %s\n' % args
                LOGGER.exception(msg)
                raise UnableToLoadSettings(msg)
