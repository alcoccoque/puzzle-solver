"""Tests for user"""

import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.parametrize(
    "payload, status_code, schema_result",
    (
        (
            {
                "username": "test_user",
                "password": "123654",
            },
            status.HTTP_201_CREATED,
            {"username": "test_user"},
        ),
    ),
)
async def test_create_user(
    async_client: AsyncClient, payload, status_code, schema_result
):
    """Create user test case"""
    response = await async_client.post("/api/auth/register-user", json=payload)
    assert response.json() == schema_result
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code, error_msg",
    (
        (
            {
                "username": "test_user",
                "password": "123654",
            },
            status.HTTP_400_BAD_REQUEST,
            {"detail": "User with this username already exists."},
        ),
    ),
)
async def test_failed_username(
    async_client: AsyncClient, payload, status_code, error_msg
):
    """Failed username duplicate test case"""
    response = await async_client.post("/api/auth/register-user", json=payload)
    assert response.json() == error_msg
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {
                "username": "test_user",
                "password": "123654",
            },
            status.HTTP_200_OK,
        ),
    ),
)
async def test_login_user(async_client: AsyncClient, payload, status_code):
    """Create user test case"""
    response = await async_client.post(
        "/api/auth/login",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code, error_msg",
    (
        (
            {
                "username": "not_found_user",
                "password": "123654",
            },
            status.HTTP_400_BAD_REQUEST,
            {"detail": "User with this username not found."},
        ),
    ),
)
async def test_login_user_not_found(
    async_client: AsyncClient, payload, status_code, error_msg
):
    """Create user test case"""
    response = await async_client.post(
        "/api/auth/login",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.json() == error_msg
    assert response.status_code == status_code
