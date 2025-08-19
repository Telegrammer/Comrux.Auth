from abc import ABC, abstractmethod


from domain import Entity


__all__ = ["UserMapper"]


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
