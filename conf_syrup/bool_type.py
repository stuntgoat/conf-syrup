
#### Configure the config settings
# Should we treat negative values as False?
NEGATIVE_FALSE = False


def Bool(val):
    """
    Return a boolean value given an unknown value.

    """
    if isinstance(val, basestring):
        val = val.lower()
        if val in set(['0', 'false', 'no', '']):
            return False
        return True
    if isinstance(val, (int, float)):
        global NEGATIVE_FALSE
        if val:
            if NEGATIVE_FALSE and val < 0:
                return False
            return True
        return False
    return bool(val)
