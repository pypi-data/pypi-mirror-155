# source: https://stackoverflow.com/questions/6229073/how-to-make-a-dictionary-that-returns-key-for-keys-missing-from-the-dictionary-i

def DefaultDict(keygen):
    '''
    Sane **default dictionary** (i.e., dictionary implicitly mapping a missing
    key to the value returned by a caller-defined callable passed both this
    dictionary and that key).

    The standard :class:`collections.defaultdict` class is sadly insane,
    requiring the caller-defined callable accept *no* arguments. This
    non-standard alternative requires this callable accept two arguments:

    #. The current instance of this dictionary.
    #. The current missing key to generate a default value for.

    Parameters
    ----------
    keygen : CallableTypes
        Callable (e.g., function, lambda, method) called to generate the default
        value for a "missing" (i.e., undefined) key on the first attempt to
        access that key, passed first this dictionary and then this key and
        returning this value. This callable should have a signature resembling:
        ``def keygen(self: DefaultDict, missing_key: object) -> object``.
        Equivalently, this callable should have the exact same signature as that
        of the optional :meth:`dict.__missing__` method.

    Returns
    ----------
    MappingType
        Empty default dictionary creating missing keys via this callable.
    '''

    # Global variable modified below.
    global _DEFAULT_DICT_ID

    # Unique classname suffixed by this identifier.
    default_dict_class_name = 'DefaultDict' + str(_DEFAULT_DICT_ID)

    # Increment this identifier to preserve uniqueness.
    _DEFAULT_DICT_ID += 1

    # Dynamically generated default dictionary class specific to this callable.
    default_dict_class = type(
        default_dict_class_name, (dict,), {'__missing__': keygen,})

    # Instantiate and return the first and only instance of this class.
    return default_dict_class()


_DEFAULT_DICT_ID = 0
'''
Unique arbitrary identifier with which to uniquify the classname of the next
:func:`DefaultDict`-derived type.
'''