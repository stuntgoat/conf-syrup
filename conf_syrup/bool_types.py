import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('conf_syrup.bool_type')


def _to_number(val):
    try:
        i = int(val)
        f = float(val)
        if i == f:
            return i
        return f
    except Exception as e:
        LOGGER.info('failed to convert %s to valber: %s' % (val, e))


def _cast_num_to_bool(num, neg_val_false=True):
    if not num:
        return False

    if neg_val_false and num < 0:
        return False
    return True


def _yaml_bool(val):
    if not isinstance(val, basestring):
        return None
    lval = val.lower()
    if lval in {'yes', 'true'}:
        return True
    elif lval in {'no', 'false'}:
        return False


def BoolYaml(val):
    """
    Check YAML string values.

    """
    # Check if it's a number
    return _yaml_bool(val)


def BoolYamlNum(val):
    """
    Check Yaml string values; if None found, cast to a number then a bool.

    """
    res = BoolYaml(val)
    if res is not None:
        return res

    num = _to_number(val)
    if num is not None:
        return _cast_num_to_bool(num)


def Bool(val):
    """
    Default Bool is a BoolYamlNum that returns False for negative numbers.

    """
    if val is True:
        return True
    elif val is False:
        return False
    result = BoolYamlNum(val)
    if result is not None:
        return result
    LOGGER.info('unable to find boolean for %s' % val)


def BoolEmpty(val):
    """
    Returns Bool type and False on an empty string.

    """
    if isinstance(val, basestring) and not val:
        return False
    return Bool(val)


def BoolEmptyNone(val):
    """
    Returns BoolEmpty type and False on None.

    """
    if val is None:
        return False
    res = BoolEmpty(val)
    if res is not None:
        return res

    return False
