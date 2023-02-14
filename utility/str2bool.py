"""
Convert String to Boolean

Converts a set of case-insensitive truthy values to True.  Abbreviations are
not supported.  Everything else converts to False.
"""

TRUTHY = ['true', 't', 'yes', 'y', 'on']

def str2bool(value : str):
    """
    Convert string to boolean

    Arguments:
        value:
            Value to be converted.  Recognized truth values are given above.
            In addition, any decimal string that converts to a non-zero value
            is also true.  All other values are false.

    Returns:
        bool:
            The resulting boolean value.
    """
    if not isinstance(value, str):
        return False

    try:
        converted = int(value)
        return bool(converted)
    except (ValueError, TypeError):
        pass

    return value.lower() in TRUTHY
