from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Class model for local environment variables."""

    CASSANDRA_HOST: str = "127.0.0.1"
    CASSANDRA_PORT: int = 9042
    CASSANDRA_USER: str = "cassandra"
    CASSANDRA_PWD: str = "cassandra"
    CASSANDRA_KEYSPACE: str = "testing"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
