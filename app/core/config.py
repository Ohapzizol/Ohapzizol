from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SERVER_PORT: int
    SERVER_HOST: str
    MYSQL_ROOT_PASSWORD: str
    JWT_KEY: str
    JWT_EXP: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_setting():
    return Settings()
