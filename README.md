# `conf syrup`

Acquire Service settings in Python.

# `Basic Example`

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

# `INI File Key for Section Example`

```python

#### Let's get some settings from an INI file.
ini = INI_SectionKey('/etc/port_stuff.ini')
FILE = {
    # Let's get truth from 'mine' section and the 'truth_exists' key; casted to Python bool.
    'my_truth': (ini.MkBool('mine'), 'truth_exists'),

    # Let's get the 'port' key from the 'yours' section casted to an int.
    'your_port': (ini.MkInt('yours'), 'lowest'),
}

#### FILE settings override DEFAULT settings.
settings = Settings(DEFAULT, FILE)
assert settings.my_truth is True
```

# `Consul Value for Key Example`

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

```
