"""User dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app import models
from app.config import jwt_token_settings
from app.dependencies.core import DBSessionDep
from app.models.user import User
from app.orm.user import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DBSessionDep,
) -> User:
    """Get the current user by validating the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            jwt_token_settings.JWT_SECRET_KEY,
            algorithms=[jwt_token_settings.ALGORITHM],
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = await get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[models.User, Depends(get_current_user)]
