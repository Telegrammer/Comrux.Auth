from enum import StrEnum
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from utils import camel_case_to_snake_case

class Base(DeclarativeBase):
    __abstract__ = True
    
    metadata: MetaData

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
