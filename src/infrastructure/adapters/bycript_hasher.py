from domain.ports import PasswordHasher
from domain.value_objects import RawPassword, PasswordHash
from passlib.context import CryptContext




class BycryptPasswordHasher(PasswordHasher):

    def __init__(self):
        self.pwd_context: CryptContext = CryptContext(schemes=["bycript"])

    def hash(self, raw_password: RawPassword) -> PasswordHash:
        return PasswordHash.create(bytes(self.pwd_context.hash(raw_password)))
    
    def verify(self, raw_password: RawPassword, password_hash: PasswordHash) -> bool:
        return self.hash(raw_password) == password_hash