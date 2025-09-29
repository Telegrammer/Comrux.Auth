from domain import User, Email, UserId, EmailId
from domain.value_objects import EmailAddress, PhoneNumber, PasswordHash

from infrastructure.models import User as OrmUser, Email as OrmEmail
from application.ports.mappers import UserMapper

__all__ = ["SqlAlchemyUserMapper"]


class SqlAlchemyUserMapper(UserMapper[OrmUser]):

    # TODO: got runtime-like casts in mappers. Need to remove this.
    def to_dto(self, entity: User) -> OrmUser:

        email: OrmEmail = OrmEmail(
            id_=entity.email.id_,
            address=entity.email.address,
            is_verified=entity.email.is_verified,
            user_id=entity.id_,
        )
        return OrmUser(
            id_=entity.id_,
            email=email,
            phone=entity.phone,
            password_hash=entity.password_hash,
        )

    def to_domain(self, dto: OrmUser) -> User:
        email: OrmEmail = dto.email
        return User(
            id_=UserId(dto.id_.__str__()),
            email=Email(
                id_=EmailId(email.id_.__str__()),
                address=EmailAddress(email.address),
                is_verified=email.is_verified,
            ),
            phone=PhoneNumber(dto.phone),
            password_hash=PasswordHash(dto.password_hash),
        )
