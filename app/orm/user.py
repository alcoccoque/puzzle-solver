"""User ORM functions."""

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.hash_code import get_password_hash
from app.models.user import User
from app.schemas.user import CreateUser


async def get_user(username: str, db: AsyncSession):
    """Get the user by username."""
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    return result.scalar()


async def create_user(user: CreateUser, db: AsyncSession):
    """Create a new user."""
    query = (
        insert(User)
        .values(
            username=user.username,
            hashed_password=get_password_hash(user.password),
        )
        .returning(User)
    )

    result = await db.execute(query)
    created_user = result.scalar()
    await db.commit()
    return created_user
