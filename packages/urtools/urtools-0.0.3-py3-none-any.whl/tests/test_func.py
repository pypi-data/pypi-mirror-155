import logging
LOGGER = logging.getLogger(__name__)

import pytest

from urtools.functional.compose import assert_composable

def f_int_to_str(x: int) -> str:...

def f_str_to_float(x: str) -> float:...

def f_2ints_to_str(x1: int, x2: int) -> str:...

def f_returns_none() -> None:...

def f_takes_anything(x: None):...

def f_int_to_int(x: int) -> int:...

def f_float_to_float(x: float) -> float:...

#TODO: This should be doable
# def f__to_2ints() -> tuple[int, int]:...

class Test_are_composable:
    @pytest.mark.parametrize(('f1', 'f2', 'expected'),
                             ((f_int_to_str, f_str_to_float, True),
                              (f_str_to_float, f_int_to_str, False),
                              (f_2ints_to_str, f_str_to_float, True),
                              (f_str_to_float, f_2ints_to_str, False),
                              (f_returns_none, f_takes_anything, True),
                              (f_int_to_int, f_int_to_int, True),
                              (f_int_to_int, f_float_to_float, True)))
    def test(self, f1, f2, expected):
        assert assert_composable((f1, f2)) == expected

from urtools.functional.compose import compose2

def square(x: int) -> int: return x**2
def cube(x: int) -> int: return x**3
def add(x: int, y: int) -> int: return x+y

class Test_compose2:
    @pytest.mark.parametrize(('f1', 'f2', 'inputs', 'expected'),
                             ((square, cube, [1], 1),
                              (square, cube, [2], 64),
                              (add, square, [2, 3], 25)))
    def test(self, f1, f2, inputs, expected):
        assert compose2(f1, f2)(*inputs) == expected

#TODO: make it work with lambdas as well
def to_str(x: object) -> str: return str(x)
def double_str(x: str) -> str: return x+x
from urtools.functional.compose import compose
class Test_compose:
    @pytest.mark.parametrize(('functions', 'inputs', 'expected'),
                             (([square, square, square], [2], 256),
                              ([add, square], [1,2], 9),
                              ([add, lambda x:x**2, str, lambda x:x+x], [1,2], '99')
                              ))
    def test(self, functions, inputs, expected):
        assert compose(*functions)(*inputs) == expected #type:ignore

