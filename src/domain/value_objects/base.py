from abc import ABC
from dataclasses import dataclass, fields
from typing import Type


__all__ = [
    "ValueObject",
    "ValueObjectDescriptor",
]

class ValueObject: ...

@dataclass(init=False, repr=False)
class ValueObject[T](ABC):
    __slots__ = ["value"]
    value: T

    def __post_init__(self):
        if not fields(self):
            raise TypeError(f"{self.__class__.__name__} must be initialized")
    
    @classmethod
    def create(cls, value: T) -> ValueObject:
        return cls(value=value)



class ValueObjectDescriptor:
    def __init__(self, field_name: str):
        self.object_name = f"__object_{field_name}"

    def __get__(self, instance, owner: Type = None):
        if instance is None:
            return self

        class_object = getattr(instance, self.object_name)
        return class_object.value

    def __set__(self, instance: ValueObject, value) -> None:
        setattr(instance, self.object_name, value)