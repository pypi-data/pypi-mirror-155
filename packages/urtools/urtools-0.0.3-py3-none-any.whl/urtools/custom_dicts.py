"""Customized variations of the standard `dict`."""

from __future__ import annotations
from typing import Any, Dict

class ListDict(Dict[str, Any]):
    """A dictionary indexed by strings with values typecasted into lists by default.
    """
    
    def update(self, other: dict[str, Any]) -> None:
        """If the key is already present and its value is a list, 
        either the new value `v` is added to that list 
        (if `v` is not a list) or the old list is extended with `v`
        (if `v` is a list).
        """
        
        for k, v in other.items():
            assert isinstance(k, str)
            if k in self.keys() and isinstance(self[k], list):
                if isinstance(v, list):
                    self[k].extend(v)
                else:
                    self[k].append(v)
            else:
                self[k] = v

    def __getitem__(self, __k: str) -> Any:
        return super().__getitem__(__k)

class DictDict(Dict[str, dict]):
    """Nested dictionary, similar to ListDict but values are always dicts,
    instead of lists or individual values.
    """

    def update(self, other: dict[str, dict]) -> None:
        """If the key is taken, extend its dictionary.
        Otherwise, just "update yourself" with `other`. 
        """
        
        for k, v in other.items():
            assert isinstance(k, str)
            assert isinstance(v, dict)
            if k in self.keys():
                self[k].update(v)
            else:
                self[k] = v

    def __getitem__(self, __k: str) -> Any:
        return super().__getitem__(__k)

class NatDict(Dict[int, Any]):
    """A dictionary indexed with natural numbers, with key clashes prevented by `assert`.
    """
    
    def update(self, other: dict[int, Any]) -> None:
        assert all(k not in self.keys() for k in other), f"Key clashing in during attempted update!"
        assert all(isinstance(k, int) and k >= 0 for k in other), "Not all keys are natural numbers!"
        super().update(other)

    def __getitem__(self, __k: int) -> Any:
        return super().__getitem__(__k)

