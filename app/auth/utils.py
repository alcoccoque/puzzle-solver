"""Utility functions for authentication."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt

from app.config import jwt_token_settings


async def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Create the access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            jwt_token_settings.TOKEN_LIFESPAN
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        jwt_token_settings.JWT_SECRET_KEY,
        algorithm=jwt_token_settings.ALGORITHM,
    )
    return encoded_jwt
