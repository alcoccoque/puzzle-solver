"""User schemas."""

# pylint: disable=too-few-public-methods
from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    """User create schema."""

    username: str = Field(..., max_length=150)
    password: str = Field(..., min_length=3)

    class ConfigDict:
        """Config dict."""

        from_attributes = True


class GetUser(BaseModel):
    """Get user schema."""

    username: str

    class ConfigDict:
        """Config dict."""

        from_attributes = True


class UserLogin(BaseModel):
    """User login schema."""

    username: str = Field(title="username", description="username")
    password: str = Field(title="User’s password", description="User’s password")

    class ConfigDict:
        """Config dict."""

        from_attributes = True


class ResponseToken(BaseModel):
    """Response token schema."""

    access_token: str = Field(
        title="User’s access token", description="User’s access token"
    )
    token_type: str = Field(title="User’s token type", description="User’s token type")
