import logging
import json
from base64 import b64decode
from urllib2 import HTTPError, urlopen

from conf_syrup.bool_types import Bool
from conf_syrup.network_type import NetworkFromPrefix

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger('conf_syrup.consul')


class ConsulKey(object):
    def __init__(self, host, port=8500, version='v1', use_https=False):
        self.host = host
        self.port = port
        self.use_https = use_https
        self.version = version

    def _make_url(self, path):
        scheme = 'https' if self.use_https else 'http'
        return '%s://%s:%s/%s/kv/%s' % (scheme, self.host, self.port, self.version, path)

    def _decode_value(self, res):
        obj = json.loads(res)
        val = obj[0].get('Value')
        return b64decode(val)

    def _make_call(self, val):
        url = self._make_url(val)
        try:
            response = urlopen(url)
            return self._decode_value(response.read())
        except HTTPError as e:
            msg = 'Error getting key, %s, from Consul: %s' % (val, e)
            LOGGER.error(msg)
            raise

    def Int(self, key):
        return int(self._make_call(key))

    def String(self, key):
        return self._make_call(key)

    def Bool(self, key):
        return Bool(self._make_call(key))

    def Float(self, key):
        return float(self._make_call(key))

    def NetworkPrefix(self, key):
        return NetworkFromPrefix(self._make_call(key))
