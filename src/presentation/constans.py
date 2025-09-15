__all__ = ["TokenType"]


from enum import StrEnum


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
    ANY = "any"
