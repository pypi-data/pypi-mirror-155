from __future__ import annotations

from typing import Callable, TypeVar
from typing_extensions import ParamSpec

P = ParamSpec('P')
R = TypeVar('R')
def mapfunctions(functions: list[Callable[P, R]], *args: P.args, **kwargs: P.kwargs) -> list[R]:
    return [f(*args, **kwargs) for f in functions]

