from mock import patch
from pytest import raises

from conf_syrup.settings import Settings, InvalidOption
from conf_syrup.bool_types import Bool
from conf_syrup.exceptions import ConflictingTypes


class TestSettings(object):

    def test_load_settings(self):
        FIRST = {
            'hi': 1,
            'bye': 2,
        }
        SECOND = {
            'hi': 3,
            'bye': 4,
            'cat': 'dog'
        }

        settings = Settings(FIRST, SECOND)

        assert settings.hi == 3
        assert settings.bye == 4
        assert settings.cat == 'dog'

        settings = Settings(SECOND, FIRST)

        assert settings.hi == 1
        assert settings.bye == 2
        assert settings.cat == 'dog'

    def test_load_settings_missing_attr(self):
        S = {
            'hi': 1,
            'bye': 2,
        }

        settings = Settings(S)
        with raises(InvalidOption):
            assert settings.nope

    def test_settings_tuple_type_cast(self):
        with_types = {
            'is_good': (Bool, 'yes'),
            'one': (int, '11'),
            'two': (float, '22'),
        }

        settings = Settings(with_types)

        assert isinstance(settings.two, float)
        assert settings.one == 11
        assert settings.is_good is True

    def test_settings_environ_override_cast(self):
        # Inject into the environment.
        mock_env = {
            'is_good': 'no',
            'one': '11',
            'two': '3.1',
        }

        with_types = {
            'is_good': (Bool, 'yes'),
            'one': (int, 0),
            'two': (float, 0),
        }

        with patch('conf_syrup.settings.os') as pos:
            pos.environ = mock_env
            settings = Settings(with_types)
            assert settings.is_good is False
            assert settings.one == 11
            assert settings.two == 3.1

    def test_settings_environ_not_added(self):

        # Inject into the environment.
        mock_env = {
            'here': 'yes',
            'not_here': 'no',
        }

        with_types = {
            'here': (Bool, False),
        }

        with patch('conf_syrup.settings.os') as pos:
            pos.environ = mock_env
            settings = Settings(with_types)
            assert settings.here is True
            with raises(InvalidOption):
                assert settings.not_here

    def test_settings_inheritable_cast(self):

        with_types = {
            'is_good': (Bool, 'no'),
            'one': (int, 0),
            'two': (float, 0),
        }

        without_types = {
            'is_good': 'yes',
            'one': '1',
            'two': '4.3',
        }
        with patch('conf_syrup.settings.os') as pos:
            pos.environ = {}
            settings = Settings(with_types, without_types)

            assert settings.is_good is True
            assert settings.one == 1
            assert settings.two == 4.3

    def test_settings_inheritable_cast_conflict(self):

        with_types = {
            'one': (int, 0),
        }

        without_types = {
            'one': (float, 0.2),
        }

        with raises(ConflictingTypes):
            settings = Settings(with_types, without_types)

        with patch('conf_syrup.settings.os') as pos:
            pos.environ = {}
            settings = Settings(with_types, without_types, strict_types=False)
            assert settings.one == .2
