from __future__ import annotations

from typing import Callable, Literal, TypeVar, Union

from urtools.dict_tools.is_subdict import is_subdict

K = TypeVar('K')
V = TypeVar('V')
def sort_dict(d: dict[K, V], by: Literal['k', 'v', 'key', 'value'], *, 
              key: Callable | None=None, reverse: bool=False) -> dict[K, V]:
    if by[0] not in ['k', 'v']:
        raise ValueError(f'Invalid argument {by=}')
    if by[0] == 'k':
        if all(isinstance(k, (int, float)) for k in d):
            return dict(sorted(d.items(), key=key, reverse=reverse))
        else:
            key_map: dict[Union[K, V, str], Union[K, V, str]] = {str(k): k for k in d} 
            key_map.update({k: str(k) for k in d})
            d_sorted = {key_map[k]: v 
                        for k, v in sorted(
                            [(key_map[k], v) 
                             for k, v in d.items()])}
            assert is_subdict(d_sorted, d)
            return d_sorted
    else:
        # by[0] == 'v':
        d_reversed = {v: k for k, v in d.items()}
        d_sorted = {k: v for v, k in sort_dict(d_reversed, by='k', key=key, reverse=reverse).items()}
        assert is_subdict(d_sorted, d)
        return d_sorted
