from __future__ import annotations

from dataclasses import dataclass, field
from functools import reduce
from inspect import getfullargspec, isbuiltin, isclass
from typing import Callable, Iterable, Type, TypeVar
from typing_extensions import ParamSpec, TypeGuard

from urtools.functional.is_lambda import is_lambda

@dataclass
class FunctionUnannotatedReturnError(Exception):
    function_name: str
    message: str = field(init=False)
    def __post_init__(self):
        self.message = f'Function `{self.function_name}` does not have a `return` annotation.'

@dataclass
class FunctionUnannotatedArgumentsError(Exception):
    function_name: str
    message: str = field(init=False)
    def __post_init__(self):
        self.message = f'Function `{self.function_name}` does not have annotated arguments'

def _get_func_arg_names(f: Callable) -> list[str]:
    return getfullargspec(f).args

def is_privileged_callable(f: Callable) -> bool:
    return is_lambda(f) or isbuiltin(f) or isclass(f)

P = ParamSpec('P')
R1, R2 = TypeVar('R1'), TypeVar('R2')
def assert_composable(funcs: tuple[Callable, Callable]) -> TypeGuard[tuple[Callable[..., R1], Callable[[R1], R2]]]:
    """Assert that the return type of `f1` matches the argument type of `f2`.
    """
    if not isinstance(funcs, Iterable) or not all(isinstance(func, Callable) for func in funcs):
        raise TypeError('`funcs` must be a pair (2-tuple) of functions.')
    if len(funcs) != 2:
        raise ValueError('`funcs` must contain exactly two functions')
    f1, f2 = funcs

    if is_privileged_callable(f1) or is_privileged_callable(f2):
        return True
    
    # f1 return type
    if 'return' not in f1.__annotations__:
        raise FunctionUnannotatedReturnError('f1')
    f1_return_type = f1.__annotations__['return']

    if not isinstance(f1_return_type, Type):
        f1_return_type = type(f1_return_type)

    # f2 arg type    
    f2_arg_annotations = {k: (v if isinstance(v, Type) else type(v)) # subsequent conditional behavior
                          for k, v  in f2.__annotations__.items() 
                          if k != 'return'} # initial filtering
    f2_arg_names = _get_func_arg_names(f2)
    
    if sorted(f2_arg_annotations) != sorted(f2_arg_names):
        raise FunctionUnannotatedArgumentsError('f2')

    f2_first_argument_type = next(type_ for type_ in f2_arg_annotations.values())
    f2_is_one_arg = len(f2_arg_annotations) == 1
    
    types_match = issubclass(f1_return_type, f2_first_argument_type) or (f1_return_type == int and f2_first_argument_type in (float, complex))
    
    return types_match and f2_is_one_arg

def compose2(f1: Callable[P, R1], f2: Callable[[R1], R2]) -> Callable[P, R2]:
    r"""Compose two functions.

    Composability does not need to be asserted  because it is typechecked.

    .. math::
        f &: \text{dom}\;f\to T\\
        g &: T\quad\quad\to \text{ran}\;g\\
        g\circ f &: A \quad\quad\to B
    """

    def composed(*args: P.args, **kwargs: P.kwargs) -> R2:
        return f2(f1(*args, **kwargs))
    
    return composed


@dataclass
class NonComposableFunctionSequenceError(Exception):
    all_functions: Iterable[Callable]
    non_composable_function_pairs: Iterable[tuple[Callable, Callable]]
    message: str = field(init=False)
    def __post_init__(self) -> None:
        self.message = f"""\
            You provided the following functions for composition:
            {self.all_functions}
            Not all of them are composable:
            {self.non_composable_function_pairs}"""

@dataclass
class NonComposableFunctionPairError(Exception):
    f1: Callable
    f2: Callable
    message: str = field(init=False)
    def __post_init__(self) -> None:
        self.message = f"""\
            Functions {self.f1.__name__} and {self.f2.__name__} cannot be composed.
            Their full argument specifications are:
            f1: {getfullargspec(self.f1)}
            f2: {getfullargspec(self.f2)}"""

R = TypeVar('R')
def compose(*functions: Callable) -> Callable[P, R]:
    """Compose any number of `functions` (or `Callable`s more generally) passed as a list.

    But first assert their composability.
    """
    if len(functions) == 1:
        function ,= functions
        return function #type:ignore

    non_composable_function_pairs = [(f1, f2) for f1, f2 in zip(functions, functions[1:]) if not assert_composable((f1, f2))]
    if non_composable_function_pairs:
        raise NonComposableFunctionSequenceError(functions, non_composable_function_pairs)
    
    def composed(*args: P.args, **kwargs: P.kwargs) -> R:
        return reduce(compose2, functions[1:], functions[0])(*args, **kwargs) #type:ignore

    return composed
