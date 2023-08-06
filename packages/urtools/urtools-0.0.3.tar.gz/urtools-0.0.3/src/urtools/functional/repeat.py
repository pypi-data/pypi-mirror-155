from functools import wraps
from typing import Callable, TypeVar
from typing_extensions import ParamSpec

from urtools.functional.compose import assert_composable, compose, NonComposableFunctionPairError

P = ParamSpec('P')
R = TypeVar('R')
def repeat(func: Callable[P, R], n: int) -> Callable[P, R]:
    if not assert_composable((func, func)):
        raise NonComposableFunctionPairError(func, func)
    @wraps(func)
    def new_func(*args: P.args, **kwargs: P.kwargs) -> R:
        return compose(*(n*[func]))(*args, **kwargs) #type:ignore
    # new_func_str = "lambda x: {}x{}".format("f(" * n, ")" * n)
    # new_func = eval(new_func_str, {"f": func})
    return new_func
