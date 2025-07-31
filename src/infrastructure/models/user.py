from sqlalchemy.orm import mapped_column, Mapped

from .base import Base
from uuid import UUID


class User(Base):
    id_: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
