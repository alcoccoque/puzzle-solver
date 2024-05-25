"""This module contains the Matrix model."""

# pylint: disable=too-few-public-methods
from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative

metadata = MetaData()


@as_declarative()
class Base:
    """
    Base class.
    """

    id: Any
    __name__: str
    metadata = metadata

    @declared_attr
    def __tablename__(self) -> str:
        """Generate tablename from classname."""
        return self.__name__.lower()
