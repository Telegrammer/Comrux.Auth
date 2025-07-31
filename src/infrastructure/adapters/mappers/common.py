from typing import Any, Type, get_type_hints

from domain import Entity, ValueObject
from application.ports.mappers.errors import MappingError

__all__ = ["to_domain"]


def to_domain(source_object: object, target: Type[Entity]) -> Entity:

    target_attributes: dict[str, type] = get_type_hints(target)
    source_attributes: set[str]
    source_dict: dict[str, object]

    if isinstance(source_object, dict):
        source_dict = source_object.copy()
        source_attributes = source_dict.keys()
    else:
        source_attributes = get_type_hints(source_object).keys()
        source_dict = vars(source_object)

    result_attributes: dict[str, object] = {}
    for field_name, field_type in target_attributes.items():
        if field_name not in source_attributes:
            raise MappingError("Source object does not have required attribute")

        if issubclass(field_type, ValueObject):
            result_attributes[field_name] = field_type.create(source_dict[field_name])

    result = target(**result_attributes)
    return result
