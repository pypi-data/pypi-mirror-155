from inspect import getsource
from typing import Callable

def is_lambda(func: Callable) -> bool:
    return '<lambda>' in str(func)
