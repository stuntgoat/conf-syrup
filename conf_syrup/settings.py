import os

from conf_syrup.exceptions import InvalidOption


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

    def load_settings(self):
        for k, data in self._raw.iteritems():
            in_env = k in self._env
            if isinstance(data, (tuple, list)):
                _type, _value = data

                if in_env:
                    self._data[k] = _type(self._env[k])
                else:
                    self._data[k] = _type(_value)
                continue

            if in_env:
                self._data[k] = self._env[k]
            else:
                self._data[k] = data
