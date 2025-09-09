__all__ = ["UserMapper", "AccessKeyMapper"]

from abc import ABC, abstractmethod


from domain import Entity, Id


class DataMapper[Tdto](ABC):

    @abstractmethod
    def to_dto(
        self,
        entity: Entity,
    ) -> Tdto:
        raise NotImplementedError

    # TODO: don't know where to put. Need to resolve this
    @abstractmethod
    def to_string(self, id_: Id) -> str:
        raise NotImplementedError

    @abstractmethod
    def to_domain(self, dto: Tdto) -> Entity:
        raise NotImplementedError


class UserMapper[Tdto](DataMapper): ...


class AccessKeyMapper[Tdto](DataMapper): ...
