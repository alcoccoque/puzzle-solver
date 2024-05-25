"""Configuration file for the FastAPI application."""

# pylint: disable=too-few-public-methods
import os

from dotenv import load_dotenv

# Specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

# Load the environment variables from the .env file
load_dotenv(dotenv_path)

# Settings of project information.
project_settings = {
    "title": "Fast API application",
    "version": "1.0",
    "description": "FastAPI application with JWT authentication and SQLAlchemy ORM",
}


class ProdDBSettings:
    """Settings for the production database."""

    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_HOST: str = os.getenv("POSTGRES_HOST")
    DB_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME: str = os.getenv("POSTGRES_DB")
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class JWTTokenSettings:
    """Settings for JWT tokens."""

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    TOKEN_LIFESPAN: int = int(os.getenv("TOKEN_LIFESPAN", "15"))
    ALGORITHM: str = os.getenv("ALGORITHM")


class TestDBSettings:
    """Configuration file for the FastAPI application."""

    DB_USER: str = "test-user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "test_db"
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


prod_db_settings = ProdDBSettings()
jwt_token_settings = JWTTokenSettings()
test_db_settings = TestDBSettings()
