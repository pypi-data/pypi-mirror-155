from __future__ import annotations
from typing import TypeVar
from typing_extensions import TypeGuard

K = TypeVar('K')
V = TypeVar('V')
def is_subdict(sub_dict: dict, sup_dict: dict[K, V]) -> TypeGuard[dict[K, V]]:
    return set(sub_dict.items()).issubset(sup_dict.items())

