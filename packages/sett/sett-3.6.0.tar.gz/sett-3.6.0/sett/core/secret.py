from typing import Tuple, Dict, Callable, Union, TypeVar, cast, Any
import inspect
from dataclasses import is_dataclass, fields

from libbiomedit.lib.secret import Secret, reveal
from libbiomedit.lib.classify import is_secret

__all__ = ["Secret", "reveal"]


def enforce_secret_by_signature(
    f: Callable[..., Any], args: Tuple[Any, ...], kwargs: Dict[str, Any]
) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    sig = inspect.signature(f)
    sanitized_kwargs = {
        key: enforce_secret(val, sig.parameters[key].annotation)
        for key, val in kwargs.items()
    }
    sanitized_args = tuple(
        enforce_secret(val, prm.annotation)
        for val, prm in zip(args, sig.parameters.values())
    )
    return sanitized_args, sanitized_kwargs


T = TypeVar("T")


def enforce_secret(val: T, t: type) -> Union[T, Secret[str]]:
    if is_secret(t) or (  # check for Optional / Union:
        getattr(t, "__origin__", None) is Union
        and any(is_secret(t) for t in getattr(t, "__args__", ()))
        and isinstance(val, str)
    ):
        return Secret(cast(str, val))
    if is_dataclass(val) and issubclass(type(val), t):
        t = type(val)
    if is_dataclass(t):
        for f in fields(t):
            original_val = getattr(val, f.name)
            sanitized_val = enforce_secret(original_val, f.type)
            if original_val is not sanitized_val:
                setattr(val, f.name, sanitized_val)
    return val
