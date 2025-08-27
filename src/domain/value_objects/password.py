import re


from dataclasses import dataclass
from .base import ValueObject
from ..exceptions import DomainFieldError


__all__ = ["RawPassword", "PasswordHash"]


PASSWORD_MIN_LENGTH = 8
PASSWORD_HASH_MIN_LENGTH = 10
PASSWORD_HASH_MAX_LENGTH = 1024


@dataclass
class RawPassword(ValueObject[str]):

    def __post_init__(self):
        super().__post_init__()
        letter_pattern: re.Pattern = re.compile(r".*[a-zA-z]+.*")
        digit_pattern: re.Pattern = re.compile(r".*[0-9]+.*")
        special_character_pattern = re.compile(r".*[^\w].*")

        if len(self.value) < PASSWORD_MIN_LENGTH:
            raise DomainFieldError(
                f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
            )
        if not re.match(letter_pattern, self.value):
            raise DomainFieldError("Password must have at least one character")
        if not re.match(digit_pattern, self.value):
            raise DomainFieldError("Password must have at least one number")
        if not re.match(special_character_pattern, self.value):
            raise DomainFieldError("Password must have at least one special character")


@dataclass
class PasswordHash(ValueObject[bytes]):

    def __post_init__(self):
        super().__post_init__()
        if not PASSWORD_HASH_MIN_LENGTH < len(self.value) < PASSWORD_HASH_MAX_LENGTH:
            raise DomainFieldError(
                f"Password hash length must be between {PASSWORD_HASH_MIN_LENGTH} to {PASSWORD_HASH_MAX_LENGTH}"
            )
