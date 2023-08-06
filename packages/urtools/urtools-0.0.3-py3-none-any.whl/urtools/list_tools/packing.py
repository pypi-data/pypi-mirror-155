from __future__ import annotations
import logging
from typing import Iterable, TypeVar

from urtools.list_tools.base import prune_list, reduce_list
from urtools.functional import repeat
from urtools.type_tools import is_iter_and_non_str

def get_depth(x: object) -> int:
    """Get the depth of a given nested structure (lists and tuples)
    """
    if not is_iter_and_non_str(x):
        return 0
    if x == []:
        return 1
    depths = [get_depth(x_inner) for x_inner in x]
    return max(depths) + 1

T = TypeVar('T')
def pack1(x: T) -> list[T]:
    return [x]

def pack(x: object, depth_out: int | None=None) -> list:
    """Pack the input into a nested list of a given depth
    """
    if not is_iter_and_non_str(x):
        x_packed = [x]
        depth_out = 0 if depth_out is None else depth_out
    else:
        x_packed = list(x)
        depth_out = 1 if depth_out is None else depth_out

    x_depth = get_depth(x_packed)

    if x_depth == depth_out:
        return x_packed
    if x_depth > depth_out:
        return unpack_to_max_depth(x_packed, max_depth=depth_out)
    # x_depth < depth_out
    return repeat(pack1, depth_out - x_depth)(x_packed)

def unpack1(packed: Iterable[Iterable[T] | T]) -> list[T]:
    return [reduce_list(x) if is_iter_and_non_str(x) else x for x in packed] #type:ignore

def unpack_to_max_depth(packed: Iterable[Iterable[T]], *,
                        max_depth: int | None=None, prune: bool=False) -> list[T] | T:
    """Unpack an unpackable element (e.g. tuple or list)
     each unpackable element's sub-eleements are being moved to its super-/parent- element

    TODO: Expand, define behavior for some types, e.g. dictionaries
    """
    if not isinstance(packed, Iterable):
        raise TypeError(f'`packed` must be an Iterable but is {type(packed)}\n{packed=}')
    
    max_depth = 1 if max_depth is None else max_depth
    if not isinstance(max_depth, int):
        raise TypeError(f'`max_depth` must be a non-negative integer but is {type(max_depth)} ({max_depth=})')
    if max_depth < 0:
        raise ValueError(f'`max_depth` must be non-negative but is: {max_depth=}')

    # One iteration of unpacking
    unpacked = unpack1(packed)

    if prune:
        unpacked = prune_list(unpacked)

    unpacked_depth = get_depth(unpacked)
    if unpacked_depth == max_depth:
        return unpacked

    if unpacked_depth == 1 and max_depth == 0:
        if len(unpacked) == 1:
            return unpacked[0]
        if len(unpacked) == 0:
            return unpacked
        return unpacked
    
    return unpack_to_max_depth(packed, max_depth=max_depth, prune=prune)
