from __future__ import annotations
from typing import Iterable

def findall_str(text: str, substr: str) -> Iterable[int]:
    """Yields all the positions of the substring `substr` in the string `text`.

    Args
    ----------
    text : str
        Text in which we search for occurences of `substr`.

    substr : str
        A string for occurences of which we search in `text`.

    Yields
    ----------
    i : int
        Index of one occurence of `substr` in `text`.
    """
    
    i = text.find(substr)
    while i != -1:
        yield i
        i = text.find(substr, i+1)

def modify_str(
    old_str: str, new_substr: str, 
    start: int, end: int | None = None
    ) -> str:
    """Modify a string by replacing a piece of it with a new substring 
    or inserting a new substring.

    Args
    ----------
    old_str : str
        The string to be modified.
    new_substr : str
        A substring that will be inserted in the new string.
    start : int
        Position within `old_str` where `new_substr` insert starts.
    end : int | None, default=None
        Position within `old_str` where `new_substr` insert ends.
        If it is not `None`, must be greater than or equal to `start`.

    Note
    ----------
    If `end` is `None` (default value), then `new_substr` is just inserted into
    `old_str` at `start`-th position. If it is not `None`, then `new_substr` replaces 
    the segment of `old_str` from `start` to `end`. 
    """

    if end is None:
        end = start
    else:
        assert start >= 0 and start <= end
    return old_str[:start] + new_substr + old_str[end:]

def partition_n(string: str, sep: str, n: int | None=None) -> list[str]:
    if n is not None and (not isinstance(n, int) or n < 0):
        raise AssertionError(f'`n` must be a non-negative integer or `None`; {n=}')
    r1, r2, rest = string.partition(sep)
    if n is None:
        return [r1, r2, *partition_n(rest, sep)]
    if n > 0:
        return [r1, r2, *partition_n(rest, sep, n-1)]
    else: 
        # n == 0
        return [r1, r2, rest]
    