from domain import Entity, User, Uuid4, Email, PhoneNumber, PasswordHash, UserId

from infrastructure.models import User as OrmUser
from application.ports.mappers import UserMapper
from .common import to_dto


__all__ = ["SqlAlchemyUserMapper"]


class SqlAlchemyUserMapper(UserMapper[OrmUser]):

    def to_string(self, id_: UserId) -> str:
        return str(id_)

    def to_dto(self, entity: Entity) -> OrmUser:
        return to_dto(entity, OrmUser)

    def to_domain(self, dto: OrmUser) -> User:
        return User(
            id_=Uuid4(dto.id_.__str__()),
            email=Email(dto.email),
            phone=PhoneNumber(dto.phone),
            password_hash=PasswordHash(dto.password_hash),
        )
