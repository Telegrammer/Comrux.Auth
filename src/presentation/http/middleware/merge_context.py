__all__ = ["merge_context"]

from typing import Type
from dishka.async_container import CONTAINER_KEY
from dishka import DependencyKey, AsyncContainer, DEFAULT_COMPONENT

def _to_dependency_key(type_hint: Type):
    return DependencyKey(type_hint, DEFAULT_COMPONENT)

def merge_context(prev_container: AsyncContainer, extra_context: dict[DependencyKey, object | Type]) -> dict[DependencyKey, object | Type]:
    merged: dict[DependencyKey, object | Type] = {}

    for key, val in getattr(prev_container, "_context", {}).items():
        if key is CONTAINER_KEY:
            continue
        
        if isinstance(key, DependencyKey):
            merged[key] = val
        else:
            merged[_to_dependency_key(key)] = val

    for k, v in extra_context.items():
        dk = _to_dependency_key(k)
        merged[dk] = v

    return merged