from domain import Entity, User

from infrastructure.models import User as OrmUser
from application.ports.mappers import UserMapper
from .common import to_dto, to_domain


__all__ = ["SqlAlchemyUserMapper"]


class SqlAlchemyUserMapper(UserMapper[OrmUser]):

    def to_dto(self, entity: Entity) -> OrmUser:
        return to_dto(entity, OrmUser)

    def to_domain(self, dto: OrmUser) -> User:
        return to_domain(dto, User)
