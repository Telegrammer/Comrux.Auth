from domain.entities import User
from domain.value_objects import RawPassword, PasswordHash, Email, PhoneNumber
from domain.ports import PasswordHasher, UserIdGenerator


class UserService:

    def __init__(self, hasher: PasswordHasher, id_generator: UserIdGenerator):
        self._password_hasher = hasher
        self._user_id_generator = id_generator

    def create_user(self, email: Email, phone: PhoneNumber, raw_password: RawPassword) -> User:
        
        return User(
            id_= self._user_id_generator(),
            email=email,
            phone=phone,
            password_hash=self._password_hasher.hash(raw_password)
        )

    def is_password_valid(self, user: User, raw_password: RawPassword) -> bool:
        return self._password_hasher.verify(raw_password.value, user.password_hash)

    def change_password(self, user: User, new_password: RawPassword) -> None:
        new_password_hash: PasswordHash = self._password_hasher.hash(new_password)
        user.password_hash = new_password_hash
