from abc import ABCMeta
from dataclasses import dataclass
from typing import Any, TypeVar, Generic

from ..value_objects import ValueObject, ValueObjectDescriptor, Id


class ValueObjectDescriptorMeta(type):
    def __new__(cls, name, bases, dct):
        annotations = {}
        for base in reversed(bases):
            if hasattr(base, "__annotations__"):
                annotations.update(base.__annotations__)
        annotations.update(dct.get("__annotations__", {}))

        for field_name, field_type in annotations.items():
            
            if isinstance(field_type, TypeVar) and field_type.__bound__:
                field_type = field_type.__bound__
            
            if isinstance(field_type, type) and issubclass(field_type, ValueObject):
                dct[field_name] = ValueObjectDescriptor(field_name)

        return super().__new__(cls, name, bases, dct)


class EntityMeta(ABCMeta, ValueObjectDescriptorMeta):
    ...
    
@dataclass(eq=False)
class Entity[IdT: Id](metaclass=EntityMeta):

    id_: IdT

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "id_" and getattr(self, "id_", None) is not None:
            raise "Changing entity ID is not permitted." # TODO: make domain errors
        super().__setattr__(name, value)

    def __eq__(self, other: Any) -> bool:
        return type(self) is type(other) and other.id_ == self.id_

    def __hash__(self) -> int:
        return hash((type(self), self.id_))