from enum import Enum

def enum2tuple(enum: Enum, value_first=False):
    """Convert an enum **object** to a tuple (value, name)

    Args
    ----------
    enum : EnumMeta
        The `enum` to be converted into a dictionary.

    value_first : bool, default=True
        If `True`, returns (value, name) pairs. If `False`, returns (name, value) pairs.
    """

    if value_first:
        return (enum.value, enum.name)
    return (enum.name, enum.value)
