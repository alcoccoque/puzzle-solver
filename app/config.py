"""Configuration file for the FastAPI application."""

# pylint: disable=too-few-public-methods
import os

from dotenv import load_dotenv

ENV = os.getenv('ENV', 'prod')

# Set the path to the appropriate .env file
if ENV == 'test':
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.test")
else:
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

load_dotenv(dotenv_path)

# Settings of project information.
project_settings = {
    "title": "Fast API application",
    "version": "1.0",
    "description": "FastAPI application with JWT authentication and SQLAlchemy ORM",
}


class DBSettings:
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


db_settings = DBSettings()
jwt_token_settings = JWTTokenSettings()
