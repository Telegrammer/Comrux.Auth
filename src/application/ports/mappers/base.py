__all__ = ["UserMapper", "AccessKeyMapper", "EmailVerififcationMapper"]

from abc import ABC, abstractmethod


from domain import Entity, Id


class DataMapper[Tdto](ABC):

    @abstractmethod
    def to_dto(
        self,
        entity: Entity,
    ) -> Tdto:
        raise NotImplementedError

    @abstractmethod
    def to_domain(self, dto: Tdto) -> Entity:
        raise NotImplementedError


class UserMapper[Tdto](DataMapper): ...


class AccessKeyMapper[Tdto](DataMapper): ...


class EmailVerififcationMapper[Tdto](DataMapper): ...
