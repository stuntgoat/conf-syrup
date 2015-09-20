import logging
import os

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('conf_syrup.settings')

from conf_syrup.exceptions import (
    InvalidOption,
    UnableToLoadSettings,
    ConflictingTypes,
)
from conf_syrup.bool_types import Bool

INHERITABLE_TYPES = set([
    int,
    str,
    float,
    bool,
    long,
    unicode,
    Bool,
])


class Settings(object):
    def __init__(self, *confs, **kwargs):
        """
        `*confs` is one or more dictionary to be loaded in the order in which
        they are passed in.

        `kwargs` may contain:
            strict_types(True): bool, will we raise on conflicting inheritable types?
            infer_inheritable(True): bool, will we infer inheritable types?

        """
        self._raw = {}
        self._data = {}
        self._key_types = {}
        self._env = os.environ
        self.strict_types = kwargs.get('strict_types', True)
        self.infer_inheritable = kwargs.get('infer_inheritable', True)
        self.load_confs(*confs)
        self.load_settings()

    def __getattr__(self, attr):
        if attr in self._data:
            return self._data[attr]

        raise InvalidOption('%s not declared since calling load_settings!' % attr)

    def _check_conflicting_types(self, k, _type):
        # Check conflicting type info.
        found_type = self._key_types.get(k)
        if found_type and found_type != _type and self.strict_types:
            msg = 'previously found %s type for key(%s), would set as %s'
            raise ConflictingTypes(msg % (found_type, k, _type))
        self._key_types[k] = _type

    def merge_inheritable_types(self, conf):
        """
        Some keys define types and may be overridden by environment variables.
        We will load a set of inheritable types as they are defined; if the
        key is overridden from another conf, wherein the type is missing, since
        we've cached the previously defined type, we'll use that to cast the value.

        We'll raise a ConflictingTypes exception if self.strict_types is True and
        previously defined inheritable types conflict.

        """
        for k, v in conf.iteritems():
            _type = None
            if isinstance(v, (tuple, list)):
                # We've included type information.
                _type, _ = v
                if _type not in INHERITABLE_TYPES:
                    # Nothing to type check, since this type won't be inherited.
                    continue
                self._check_conflicting_types(k, _type)

            # Type information not included, let's check.
            if k in self._key_types:
                # We have a type.
                continue

            if not self.infer_inheritable:
                # We don't have a type but we're not going to infer types either.
                continue

            # Type information was not supplied so we'll infer
            inferred = type(v)
            if inferred not in INHERITABLE_TYPES:
                continue

            self._key_types[k] = inferred

    def load_confs(self, *confs):
        for conf in confs:
            self.merge_inheritable_types(conf)
            self._raw.update(conf)

    @classmethod
    def cast_type(cls, value, _type):
        if _type:
            return _type(value)
        return value

    def _load_key(self, k, data):
        """
        There are 3 choices for a key:

        1. found in the environment
         - we'll attempt to find a type to cast it as.

        2. Supplied type information
         - we'll cast the value accordingly

        3. not found in the environment and no supplied type information.
         - we'll attempt to find a type to cast it as.

        """
        # Find an inheritable type.
        found_type = self._key_types.get(k)

        if k in self._env:
            self._data[k] = self.cast_type(self._env[k], found_type)
            return

        if not isinstance(data, (tuple, list)):
            # No type information supplied.
            self._data[k] = self.cast_type(data, found_type)
            return

        # Type was supplied.
        _type, value = data
        self._data[k] = self.cast_type(value, _type)

    def load_settings(self):
        for k, data in self._raw.iteritems():
            try:
                self._load_key(k, data)
            except Exception as e:
                args = (k, data, e)
                msg = 'Unable to load value for key: %s with data: %s Error: %s\n' % args
                LOGGER.exception(msg)
                raise UnableToLoadSettings(msg)
