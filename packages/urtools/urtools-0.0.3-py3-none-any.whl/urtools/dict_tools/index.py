from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Hashable, Iterable, List, Literal, TypeVar, Union, cast

from urtools.list_tools.list_nans import list_has_nans
from urtools.dict_tools.join_dicts import join_dicts
from urtools.type_tools import is_iter

@dataclass
class DictInvalidKeyError(Exception):
    invalid_key: Hashable
    d: dict
    message: str = field(init=False)
    def __post_init__(self):
        d = self.d
        self.message = f'This dictionary has an invalid key: {self.invalid_key}\n{d=}'

class KeysAndNegKeysAreNoneError(Exception):
    message: str = field(init=False)
    def __post_init__(self):
        self.message = f'Either `keys` or `neg_keys` must be `None` but here both are `None`.'

class KeysAndNegKeysAreNotNoneError(Exception):
    keys: Union[Hashable, Iterable[Hashable]]
    neg_keys: Union[Hashable, Iterable[Hashable]]
    message: str = field(init=False)
    def __post_init__(self):
        keys = self.keys
        neg_keys = self.neg_keys
        self.message = f'You can pass either `keys` or `neg_keys` to this function:\n{keys = }\n{neg_keys = }'

class NoneInKeysError(Exception):
    keys_or_neg_keys: Literal['keys', 'neg_keys']
    k: Iterable[Hashable]
    message: str = field(init=False)    
    def __post_init__(self):
        self.message = f'`{self.keys_or_neg_keys}` contains an invalid value `None`'

class DictInvalidValueError(Exception):
    d: dict
    message: str = field(init=False)
    def __post_init__(self):
        d = self.d
        self.message = f'This dictionary has `None`-ish values:\n{d=}'

K = TypeVar('K')
V = TypeVar('V')
Keys = List[K]
def _dict_multindex_prep_keys(d: dict[K, Any], keys: Union[K, Iterable[K], None] = None, *,
                              neg_keys: Union[K, Iterable[K], None] = None) -> Keys:
    if None in d:
        raise DictInvalidKeyError(None, d)
    if keys is None and neg_keys is None:
        raise KeysAndNegKeysAreNoneError()
    if keys is not None and neg_keys is not None:
        raise KeysAndNegKeysAreNotNoneError(keys, neg_keys)
    if is_iter(keys) and list_has_nans(cast(Iterable, keys)):
        raise NoneInKeysError('keys', keys)
    if is_iter(neg_keys) and list_has_nans(cast(Iterable, neg_keys)):
        raise NoneInKeysError('neg_keys', neg_keys)
    
    # keys
    if keys is None:
        keys = list(d)
    elif isinstance(keys, str) or not isinstance(keys, Iterable):
        keys = [keys] #type:ignore
    # neg_keys
    if neg_keys is None:
        neg_keys = []
    elif not isinstance(neg_keys, Iterable):
        neg_keys = [neg_keys]

    assert isinstance(keys, Iterable)
    return sorted(set(keys).difference(neg_keys), key=str) 
    
def dict_multindex(d: dict[K, V], keys: K | Iterable[K] | None=None, *,
                   neg_keys: K | Iterable[K] | None=None) -> dict[K, V]:
    # PREP KEYS:
    keys = _dict_multindex_prep_keys(d, keys=keys, neg_keys=neg_keys)
    return {k: d[k] for k in keys}

def dict_del_keys(d: dict[K, V], del_keys: K | Iterable[K]) -> dict[K, V]:
    if not isinstance(del_keys, Iterable) or isinstance(del_keys, str):
        return {k: v for k, v in d.items() if k != del_keys}
    return {k: v for k, v in d.items() if k not in del_keys}

def _dict_list_has_nans(dl: Iterable[dict]) -> bool:
    return any(list_has_nans(d.values()) for d in dl)

#TODO: optional non-nones?
def dict_list_index(dl: Iterable[dict[K, V]], key: K) -> list[V | None]:
    if _dict_list_has_nans(dl):
        d = next(filter(lambda d: list_has_nans(d.values()), dl))
        raise DictInvalidValueError(d)
    return [d.get(key) for d in dl]

#TODO: optional non-nones?
def dict_list_multindex(dl: Iterable[dict[K, V]], keys: Union[K, Iterable[K], None] = None, *,
                        neg_keys: Union[K, Iterable[K], None] = None) -> dict[K, list[Union[V, None]]]:
    keys = _dict_multindex_prep_keys(d=join_dicts(*dl), keys=keys, neg_keys=neg_keys)
    return {k: [d.get(k) for d in dl]
            for k in keys}
