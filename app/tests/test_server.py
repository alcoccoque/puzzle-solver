"""Test the server routes"""

import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.parametrize(
    "payload, status_code, result",
    (
        (
            {
                "rows": [
                    [1, 0, 2, 0, 0],
                    [0, 5, 0, 0, 0],
                    [1, 0, 0, 0, 4],
                    [0, 0, 1, 0, 0],
                    [0, 0, 7, 0, 1],
                ]
            },
            status.HTTP_200_OK,
            [
                [1, 5, 2, 2, 4],
                [5, 5, 5, 7, 4],
                [1, 3, 5, 7, 4],
                [3, 3, 1, 7, 4],
                [7, 7, 7, 7, 1],
            ],
        ),
    ),
)
async def test_solve_puzzle(
    async_client: AsyncClient, user_token, payload, status_code, result
):
    """Test solving a puzzle"""
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = await async_client.post("/api/solve", json=payload, headers=headers)
    assert resp.status_code == status_code
    data = resp.json()
    assert "coordinates" in data
    solved_puzzle = data["coordinates"]
    assert solved_puzzle == result


@pytest.mark.parametrize(
    "payload, status_code, error_msg",
    (
        (
            {
                "rows": [
                    [1, 0, 2, 0, 0],
                    [0, "invalid", 0, 0, 0],
                    [1, 0, 0, 0, 4],
                    [0, 0, 1, 0, 0],
                    [0, 0, 7, 0, 1],
                ]
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "type": "int_parsing",
                        "loc": ["body", "rows", 1, 1],
                        "msg": "Input should be a valid integer, "
                        "unable to parse string as an integer",
                        "input": "invalid",
                    }
                ]
            },
        ),
    ),
)
async def test_solve_puzzle_invalid_type(
    async_client: AsyncClient, user_token, payload, status_code, error_msg
):
    """Test invalid puzzle"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.post("/api/solve", json=payload, headers=headers)
    assert response.json() == error_msg
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code, error_msg",
    (
        (
            {
                "rows": [
                    [1, 0, 2, 0, 0],
                    [0, 1, 1, 0, 0],
                    [1, 0, 0, 0, 4],
                    [0, 0, 1, 0, 0],
                    [0, 0, 7, 0, 1],
                ]
            },
            status.HTTP_400_BAD_REQUEST,
            {"detail": "Wrong group size"},
        ),
    ),
)
async def test_solve_puzzle_invalid_value(
    async_client: AsyncClient, user_token, payload, status_code, error_msg
):
    """Test invalid puzzle"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.post("/api/solve", json=payload, headers=headers)
    assert response.json() == error_msg
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code, error_msg",
    (
        (
            {"rows": [[1, 0, 2, 0, 0]]},
            status.HTTP_400_BAD_REQUEST,
            {"detail": "Minimum field size is 2"},
        ),
    ),
)
async def test_solve_puzzle_invalid_size(
    async_client: AsyncClient, user_token, payload, status_code, error_msg
):
    """Test invalid puzzle"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.post("/api/solve", json=payload, headers=headers)
    assert response.json() == error_msg
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code, board_size",
    (
        (
            {"size": 5, "filled_percentage": 0.5},
            status.HTTP_200_OK,
            5,
        ),
    ),
)
async def test_generate_test_data(
    async_client: AsyncClient, user_token, payload, status_code, board_size
):
    """Test generating test data"""
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = await async_client.get("/api/generate", headers=headers, params=payload)
    assert resp.status_code == status_code
    data = resp.json()
    assert "coordinates" in data
    test_board = data["coordinates"]
    assert len(test_board) == board_size
