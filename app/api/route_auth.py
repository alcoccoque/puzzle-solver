"""This module contains the routes for the authentication of the user."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.hash_code import verify_password
from app.auth.utils import create_access_token
from app.dependencies.core import DBSessionDep
from app.orm.user import create_user, get_user
from app.schemas.user import CreateUser, GetUser, ResponseToken

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=ResponseToken, status_code=status.HTTP_200_OK)
async def login(
    db: DBSessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Authenticate the user and return the access token."""
    user = await get_user(username=form_data.username, db=db)
    if not user:
        raise HTTPException(
            status_code=400, detail="User with this username not found."
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register-user",
    response_model=GetUser,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user: CreateUser, db: DBSessionDep):
    """Register a new user."""
    is_username_found = await get_user(username=user.username, db=db)
    if is_username_found:
        raise HTTPException(
            status_code=400, detail="User with this username already exists."
        )

    user = await create_user(user=user, db=db)
    return user
