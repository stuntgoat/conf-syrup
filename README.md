# `conf syrup`

Acquire Service settings in Python.

## `Basic Example`

```python
from conf_syrup import (
    Settings,
    Bool,
    INI_SectionKey,
    ConsulKey,
)

#### Here are the default settings.
DEFAULT = {
    'my_truth': False,
    'your_truth': False,
    'my_port': 6666,
    'your_port': 7777,
}
settings = Settings(DEFAULT)
assert settings.my_port = 6666
assert settings.my_truth = False
```

## `INI File Key for Section Example`

```python

#### Let's get some settings from an INI file.
ini = INI_SectionKey('/etc/port_stuff.ini')
FILE = {
    # Let's get truth from 'mine' section and the 'truth_exists' key; casted to Python bool.
    'my_truth': (ini.MkBool(my service'), 'truth_exists'),

    # Let's get the 'port' key from the 'yours' section casted to an int.
    'your_port': (ini.MkInt('your service'), 'lowest_port'),
}

#### FILE settings override DEFAULT settings.
settings = Settings(DEFAULT, FILE)
assert settings.my_truth is True
assert settings.your_port == 80
```

## `Consul Value for Key Example`

```python

#### Let's get settings from the Consul REST API running on localhost.
ck = ConsulKey('127.0.0.1')
CONSUL = {
    'my_port': (ck.Int, 'cluster/mine/ports/default'),

    # Let's get this value from the Consl REST API and cast it to an int.
    'your_truth': (ck.Bool, 'cluster/yours/booleans/default'),
}

#### Now we'll load all the settings and merge in the
#### order we pass them to Settings, ie., FILE settings
#### override DEFAULT settings and
#### CONSUL settings override FILE settings.
settings = Settings(DEFAULT, FILE, CONSUL)

assert settings.my_port == 9999  # Was set from Consul
assert settings.my_truth is True
assert settings.your_truth is True

```

## `Environment variable override example`

Our script `example.py`:

```python
from conf_syrup import (
    Settings,
    Bool,
)

DEFAULT = {
    'port': 80,
}

CONFIG = {
    'port': (int, 8080),
    'use_strict': (Bool, False),
}


if __name__ == '__main__':
    settings = Settings(DEFAULT, CONFIG)
    print 'port', settings.port
    print 'use_strict', settings.use_strict
    print 'DONE'
```

Environment variables override all other configs.

```shell
$ python example.py
port 8080
use_strict False
DONE
$ use_strict=yes port=9999 python example.py
port 8080
use_strict True
DONE
$
```
