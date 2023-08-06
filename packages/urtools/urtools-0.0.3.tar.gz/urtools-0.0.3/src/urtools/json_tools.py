from __future__ import annotations

import json
from typing import Literal, overload, Type, TypeVar, Union

JsonType = Union[Type[list], Type[dict]]
JsonMode = Literal['r', 'w', 'x']

# load
@overload
def load_json(path: str, json_type=dict) ->  dict: 
    ...

@overload
def load_json(path: str, json_type=list) ->  list: 
    ... 

def load_json(path: str, json_type: JsonType=dict, *, 
              mode: JsonMode='r', encoding: Union[str, None] = 'utf-8') -> list | dict:
    """Load the file into JSON in one line with context manager.
    """
    with open(path, mode, encoding=encoding) as f:
        loaded = json.load(f)
    if not isinstance(loaded, json_type):
        raise AssertionError(f'{path} is {type(loaded)}, should be {json_type}')
    return loaded

def load_dict(path: str) -> dict:
    return load_json(path, dict)

def load_list(path: str) -> list:
    return load_json(path, list)

def load_list_of_dicts(path: str) -> list[dict]:
    loaded = load_list(path)
    assert all(isinstance(x, dict) for x in loaded)
    return loaded

# dump
def dump_json(obj: list | dict, path: str) -> None:
    """Load data into a JSON file in one line with context manager.
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f)

# utils
V = TypeVar('V')
def jsonKeys2int(x: dict[str, V]) -> dict[str | int, V]:
    """A util to convert json objects' keys from strings to ints (where they should be ints)
    """
    if isinstance(x, dict):
        assert all(str(k).isdigit() and float(k) == int(k) for k in x)
        return {int(k): v for k, v in x.items()}
    return x
