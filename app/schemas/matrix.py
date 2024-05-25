"""This module contains the schemas for the matrix model."""

# pylint: disable=too-few-public-methods
from typing import List

from pydantic import BaseModel, Field


class CreateMatrix(BaseModel):
    """Create matrix schema."""

    coordinates: List[List[int]] = Field(..., min_length=1, max_length=400)
    user_id: int = Field(...)

    class ConfigDict:
        """Config dict."""

        from_attributes = True
        arbitrary_types_allowed = True


class ShowMatrix(BaseModel):
    """Show matrix schema."""

    id: int
    coordinates: List[List[int]]
    user_id: int

    class ConfigDict:
        """Config dict."""

        from_attributes = True


class SolveMatrix(BaseModel):
    """Solve matrix schema."""

    rows: List[List[int]]

    class ConfigDict:
        """Config dict."""

        from_attributes = True


class GenerateMatrix(BaseModel):
    """Generate matrix schema."""

    size: int = Field(6, gt=0, le=10)
    filled_percentage: float = Field(0.5, gt=0, le=1)

    class ConfigDict:
        """Config dict."""

        from_attributes = True
