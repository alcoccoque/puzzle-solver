"""User model."""

# pylint: disable=too-few-public-methods
from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_class import Base

if TYPE_CHECKING:
    from .matrix import Matrix


class User(Base):
    """User model."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    matrices: Mapped[List["Matrix"]] = relationship("Matrix", back_populates="user")
