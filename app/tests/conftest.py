"""Conftest module."""

import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.models.base_class import Base, metadata


def db_setup():
    os.environ["ENV"] = "test"
    from app.config import db_settings
    engine_test = create_async_engine(db_settings.DATABASE_URL)
    async_session = async_sessionmaker(
        engine_test, expire_on_commit=False, class_=AsyncSession
    )
    metadata.bind = engine_test
    return async_session, engine_test


async_session, engine_test = db_setup()


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Override default session."""
    async with async_session() as session:
        yield session


from app.db import get_async_session
app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    """Prepare test db."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    """Event loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Async client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# pylint: disable=redefined-outer-name
@pytest_asyncio.fixture
async def user_token(async_client):
    """Fixture to get the user token."""
    test_user = {"username": "test", "password": "123"}

    await async_client.post("/api/auth/register-user", json=test_user)
    res = await async_client.post(
        "/api/auth/login",
        data=test_user,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    data = res.json()

    return data["access_token"]
