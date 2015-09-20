from uuid import uuid4
from os.path import abspath

from pytest import raises

from conf_syrup.exceptions import IOErrorWhileReading
from conf_syrup.other_types import (
    SafeValFromFile,
    ValFromFile,
)

FPATH = abspath('tests/on_disk_content.txt')


class TestOtherTypes(object):
    def test_valfromfile(self):
        val = ValFromFile(FPATH)
        assert val == 'VALUE'

    def test_valfromfile_raises(self):
        with raises(IOErrorWhileReading):
            ValFromFile(str(uuid4()))

    def test_safe_valfromfile(self):
        val = SafeValFromFile(str(uuid4()))
        assert val == ''
