from __future__ import annotations

from typing import Literal

def getfields(x: object) -> list[str]:
    return [f for f in dir(x) if f[0].islower()]

def showattrs(x: object, *, mode: Literal[0, 1, 2] = 0) -> list[str]:
    """Show attributes of `x`.

    Args
    ----------
    x : object
        The object whose attributes are supposed to be shown.

    mode : Literal[0, 1, 2], default=0
        - 0 - Show only attributes that don't start with an underscore ('_')
        - 1 - Show only attributes that don't start with an dunder / double underscore ('__')
        - 2 - Show all attributes, no filtering
    """
    
    attrs = dir(x)
    if mode == 0:
        return [a for a in attrs if not a.startswith('_')]
    if mode == 1:
        return [a for a in attrs if not a.startswith('__')]
    return attrs