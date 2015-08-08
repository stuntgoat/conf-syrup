from pytest import raises

from conf_syrup.settings import Settings, InvalidOption


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
