from conf_syrup.bool_types import (
    Bool,
)
TRUE = ['1', 'YES', 'TRUE', 'True', True, 'TruE', 1, 1000, .01]
FALSE = ['0', '-1', -1, -1.1, False, 'FALSE', 'False', 'FalsE']


class TestBool(object):
    def test_false_bool(self):
        for f in FALSE:
            assert Bool(f) is False
        assert Bool('') is None

    def test_true_bool(self):
        for t in TRUE:
            assert Bool(t) is True
