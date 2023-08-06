from __future__ import annotations

from functools import reduce
from operator import add
from typing import Iterable, TypeVar

T = TypeVar('T')
def batch_split(data: list[T], batch_size: int=20) -> list[list[T]]:
    return [data[i*batch_size : (i+1)*batch_size] for i in range((len(data) // batch_size) + 1)]

def reduce_list(ll: Iterable[Iterable[T]]) -> list[T]:
    """Reduce a list - remove one level of nesting.
    """
    return reduce(add, ll) if ll else []

def split_list(l: list[T], n_splits: int) -> list[list[T]]:
    """Partition a list into `n_splits` sublists of equal size.
    """
    return [a.tolist() for a in np.array_split(l, n_splits)] #type: ignore
    
def prune_list(l: list[T]) -> list[T]:
    """Strip the list from repeating elements.
    """
    return list(dict.fromkeys(l))
