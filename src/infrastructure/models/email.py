__all__ = ["Email"]


from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from .base import Base

class User: ...

class Email(Base):
    id_: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id_"))
    user: Mapped["User"] = relationship(back_populates="email", uselist=False)

    address: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(nullable=False)
