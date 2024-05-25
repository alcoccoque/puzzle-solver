"""This module contains the Matrix model."""

# pylint: disable=too-few-public-methods
from typing import TYPE_CHECKING, List

from sqlalchemy import JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_class import Base

if TYPE_CHECKING:
    from .user import User


class Matrix(Base):
    """Matrix model."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    coordinates: Mapped[List[List[int]]] = mapped_column(
        JSON, unique=False, nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="matrices")
