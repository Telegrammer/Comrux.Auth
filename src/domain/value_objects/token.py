from dataclasses import dataclass
from .base import ValueObject
from ..exceptions import DomainFieldError


TOKEN_MIN_LENGTH = 32
TOKEN_MAX_LENGTH = 128
TOKEN_HASH_MIN_LENGTH = 32
TOKEN_HASH_MAX_LENGTH = 64

@dataclass
class Token(ValueObject[str]):

    def __post_init__(self):
        super().__post_init__()
        if not (TOKEN_MIN_LENGTH <= len(self.value) <= TOKEN_MAX_LENGTH):
            raise DomainFieldError(
                f"Token length must be between {TOKEN_MIN_LENGTH} and {TOKEN_MAX_LENGTH}"
                f" got {len(self.value)}"
            )

@dataclass
class TokenHash(ValueObject[bytes]):

    def __post_init__(self):
        super().__post_init__()
        if not (TOKEN_HASH_MIN_LENGTH <= len(self.value) <= TOKEN_HASH_MAX_LENGTH):
            raise DomainFieldError(
                f"Hash length must be between {TOKEN_HASH_MIN_LENGTH} and {TOKEN_HASH_MAX_LENGTH}"
                f" got {len(self.value)}"
            )
