from typing import Iterable

def list_has_nans(l: Iterable) -> bool:
    return any(x is None or x != x or str(x).lower() == 'nan' for x in l)