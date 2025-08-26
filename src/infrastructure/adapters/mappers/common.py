from typing import Type, get_type_hints, TypeVar

from domain import Entity, ValueObject
from application.ports.mappers import MappingError
from automapper import mapper

__all__ = ["to_dto", "to_domain"]


def to_dto(source_entity: Entity, target: Type) -> object:
    return mapper.to(target).map(source_entity)


from typing import (
    Any,
    Type,
    TypeVar,
    get_type_hints,
    get_origin,
    get_args,
    Annotated,
    ClassVar,
)


def _strip_annotated(tp):
    origin = get_origin(tp)
    if origin is Annotated:
        return get_args(tp)[0]
    return tp


def _build_typevar_map(cls: type) -> dict[TypeVar, Any]:
    """
    Собирает отображение типа: {IdT: UserId, ...} по всей иерархии __orig_bases__.
    Работает, если есть что-то вроде: class User(Entity[UserId]): ...
    """
    mapping: dict[TypeVar, Any] = {}
    for parent in cls.__mro__:
        for base in getattr(parent, "__orig_bases__", ()):
            origin = get_origin(base)
            if origin is None:
                continue
            params = getattr(origin, "__parameters__", ())
            args = get_args(base)
            # Раскрываем уже известные typevar’ы в аргументах
            resolved_args = tuple(mapping.get(a, a) for a in args)
            for p, a in zip(params, resolved_args):
                mapping[p] = a
    return mapping


def _substitute_typevars(tp: Any, mapping: dict[TypeVar, Any]) -> Any:
    """
    Меняет TypeVar на конкретный тип. Для наших целей достаточно вернуть класс,
    чтобы работал issubclass(..., ValueObject).
    """
    tp = _strip_annotated(tp)

    if isinstance(tp, TypeVar):
        return mapping.get(tp, tp.__bound__ or Any)

    origin = get_origin(tp)
    if origin is None:
        # Обычный класс — оставляем как есть
        return tp

    # Контейнеры (list[...], dict[...], Union[...]) нам для ValueObject не нужны
    # как целевой класс, поэтому оставляем без реконструкции.
    return tp


def to_domain(source_object: object, target: Type["Entity"]) -> "Entity":
    # Аннотации целевого класса (могут содержать TypeVar)
    target_hints = get_type_hints(target)
    typevar_map = _build_typevar_map(target)

    if isinstance(source_object, dict):
        source_dict = dict(source_object)
    else:
        source_dict = vars(source_object)

    result_kwargs: dict[str, Any] = {}
    for field_name, anno in target_hints.items():
        # Пропускаем ClassVar и служебные
        if get_origin(anno) is ClassVar:
            continue

        if field_name not in source_dict:
            raise MappingError(
                f"Source object does not have required attribute '{field_name}'"
            )

        field_type = _substitute_typevars(anno, typevar_map)
        value = source_dict[field_name]

        if isinstance(field_type, type) and issubclass(field_type, ValueObject):
            result_kwargs[field_name] = field_type.create(value)
        else:
            result_kwargs[field_name] = value

    return target(**result_kwargs)
