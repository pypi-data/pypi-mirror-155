from __future__ import annotations

from typing import Iterable
from typing_extensions import TypeGuard

def is_str(x: object) -> TypeGuard[str]:
    return isinstance(x, str)

def is_iter(x: object) -> TypeGuard[Iterable]:
    return isinstance(x, Iterable)

def is_str_or_non_iter(x: object) -> TypeGuard[str | Iterable]:
    return is_str(x) or not is_iter(x)

def is_iter_and_non_str(x: object) -> TypeGuard[Iterable]:
    """Is this an iterable but not a string?
    """
    return not is_str(x) and is_iter(x)


# To restore in later versions (maybe?)
# def issubtype(sub: type, 
#               sup: Union[type, tuple[type, tuple[type, ...], ...]]
#               ) -> bool:
#     """Check whether the type `sub` properly narrows down the type (or tuple of types) `sup`.
#     """
    
#     if isinstance(sup, tuple):
#         return any(issubtype(sub, sup_) for sup_ in sup)
    
#     # The most basic case
#     if not (isinstance(sub, GenericAlias) or isinstance(sup, GenericAlias)
#         ) and issubclass(sub, sup):
#         return True
    
#     # If `sub` and `sup` were not created using the same functor`
#     if get_origin(sub) != get_origin(sup):
#         return False
        
#     sup_args = get_args(sup)
#     sub_args = get_args(sub)

#     if sup_args == sub_args == ():
#         return False

#     if all(
#         any( issubtype(sub_arg, sup_arg) for sup_arg in sup_args
#             ) for sub_arg in sub_args):
#         return True
    
#     return False
