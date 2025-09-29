from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from .email import Email


class User(Base):
    id_: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[Email] = relationship(back_populates="user", uselist=False, lazy="joined")
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
