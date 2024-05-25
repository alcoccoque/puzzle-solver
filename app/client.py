"""Client integration tests module."""

import asyncio

import httpx

test_data = [
    [1, 0, 2, 0, 0],
    [0, 5, 0, 0, 0],
    [1, 0, 0, 0, 4],
    [0, 0, 1, 0, 0],
    [0, 0, 7, 0, 1],
]

test_data = [[1, 0, 2, 0, 0]]

APP_PORT = "8000"
NEW_USER = {"username": "testuser", "password": "testpassword"}


async def register_user():
    """Register a new user."""
    user = {"username": "testuser", "password": "testpassword"}
    async with httpx.AsyncClient() as client:
        print(f"http://localhost:{APP_PORT}/api/auth/register-user")
        response = await client.post(
            f"http://localhost:{APP_PORT}/api/auth/register-user", json=user
        )
        if response.status_code == 200:
            print(f"User registered with ID: {response.json()}")
            return True
        print(f"Error: ({response.status_code}): {response.text}")
        return False


async def get_auth_token():
    """Get authentication token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:{APP_PORT}/api/auth/login",
            data={"username": NEW_USER["username"], "password": NEW_USER["password"]},
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        print(f"Error: ({response.status_code}): {response.text}")
        return None


async def send_data(token):
    """Send request to /solve route."""
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(
                f"http://localhost:{APP_PORT}/api/solve",
                json={"rows": test_data},
                headers=headers,
            )
            if response.status_code == 200:
                data = response.json()
                print("Solved puzzle received from /solve route")
                coordinates = data["coordinates"]
                for row in coordinates:
                    print(row)
            else:
                print(f"Error: ({response.status_code}): {response.text}")
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")


async def generate_test_data(token):
    """Send request to /generate route."""
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            params = {"size": 7, "filled_percentage": 0.2}
            response = await client.get(
                f"http://localhost:{APP_PORT}/api/generate",
                headers=headers,
                params=params,
            )
            if response.status_code == 200:
                data = response.json()
                coordinates = data["coordinates"]
                print("Test board received from /generate route")
                for row in coordinates:
                    print(row)
            else:
                print(f"Error: ({response.status_code}): {response.text}")
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")


async def main():
    """Execute main loop."""
    registered = await register_user()
    registered = True
    if registered:
        token = await get_auth_token()
        if token:
            await send_data(token)
            await generate_test_data(token)


if __name__ == "__main__":
    asyncio.run(main())
