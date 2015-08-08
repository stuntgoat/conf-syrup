# `conf syrup`

Acquire Service settings in Python.

# `Example`
```python
from conf_syrup import (
    Settings,
    Bool,
    INI_SectionKey,
    ConsulKey,
)

#### Here are the default settings.
DEFAULT = {
    'my_host': 'localhost',
    'your_host': '10.10.10.10'
    'my_port': 6666,
    'your_port': 7777,
}

#### Let's get some settings from an INI file.
ini = INI_SectionKey('/etc/port_stuff.ini')
FILE = {
    # Let's get the 'port key from the 'mine' section.
    'my_port': (ini.MkString('mine'), 'better'),

    # Let's get the 'port' key from the 'yours' section.
    'your_port': (ini.MkInt('yours'), 'lowest'),
}

#### Let's get settings from the Consul REST API running on localhost.
ck = ConsulKey('127.0.0.1')
CONSUL = {
    # Let's  key from the 'mine' section.
    'my_port': (ck.Int, ''cluster/mine/ports/best'),

    # Let's get this value from the Consl REST API and cast it
    # to an int.
    'your_port': (ck.Int, ''cluster/yours/ports/default'),
}

#### Now we'll load all the settings and merge in the
#### order we pass them to Settings, ie., FILE settings
#### override DEFAULT settings and
#### CONSUL settings override FILE settings.
settings = Settings(DEFAULT, FILE, CONSUL)

assert settings.my_port == 988998  # Was set from Consul
assert isintance(settings.my_port, int) is True
