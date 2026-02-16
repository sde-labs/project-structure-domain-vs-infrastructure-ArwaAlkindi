"""
Configuration settings loaded from environment variables.
"""
import os

from dotenv import load_dotenv
from pydantic import BaseModel, field_validator


class Settings(BaseModel):
    """
    Application configuration sourced from environment variables.

    TODO (Week 3): Implement the following:
    - from_env classmethod to read required env vars
    - validators for env, database_url, and api_token
    """
    env: str
    database_url: str
    api_token: str

    @classmethod
    def from_env(cls):
        """
        Build Settings from environment variables.

        Local development reads from `.env` via python-dotenv.
        CI (GitHub Actions) should provide the same keys as environment variables.

        Required variables:
        - APP_ENV
        - DATABASE_URL
        - API_TOKEN

        TODO: Implement reading and missing-variable handling.
        """

        env = os.getenv("APP_ENV")
        database_url = os.getenv("DATABASE_URL")
        api_token = os.getenv("API_TOKEN")

        if env is None or database_url is None or api_token is None:
            load_dotenv()
            env = os.getenv("APP_ENV")
            database_url = os.getenv("DATABASE_URL")
            api_token = os.getenv("API_TOKEN")

        if env is None:
            raise ValueError("Missing required environment variable: APP_ENV")

        if database_url is None:
            raise ValueError("Missing required environment variable: DATABASE_URL")

        if api_token is None:
            raise ValueError("Missing required environment variable: API_TOKEN")

        return cls(
            env=env,
            database_url=database_url,
            api_token=api_token,
        )


    # TODO: Add @field_validator for env
    # Valid values: "dev", "test", "prod"
    @field_validator("env")
    def validate_env(cls, v):
        if v not in {"dev", "test", "prod"}:
            raise ValueError("env must be one of: dev, test, prod")
        return v

    # TODO: Add @field_validator for database_url
    # Must end with .db and not be empty
    @field_validator("database_url")
    def validate_database_url(cls, v):
        if v.strip() == "":
            raise ValueError("database_url must not be empty")
        if not v.endswith(".db"):
            raise ValueError("database_url must end with .db")
        return v

    # TODO: Add @field_validator for api_token
    @field_validator("api_token")
    def validate_api_token(cls, v):
        if v.strip()=="":
            raise ValueError("api_token must not be empty")
        return v  
