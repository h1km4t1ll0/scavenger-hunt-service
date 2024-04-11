import os
from os import environ, path

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):

    ENV: str = environ.get("ENV", "local")

    MONGO_DB: str = environ.get("MONGO_DB", "scavenger_hunt_storage")
    MONGO_HOST: str = environ.get("MONGO_HOST", "localhost")
    MONGO_USER: str = environ.get("MONGO_USER", "user")
    MONGO_PORT: int = int(environ.get("MONGO_PORT"[-4:], 27017))
    MONGO_PASSWORD: str = environ.get("MONGO_PASSWORD", "password")

    PROJECT_PATH: str = environ.get(
        "PROJECT_PATH", path.abspath(os.getcwd())
    )

    SRC_PREFIX: str = environ.get(
        "SRC_PREFIX", f'{PROJECT_PATH}/src/'
    )
    PRESETS_PREFIX: str = environ.get(
        "PRESETS_PREFIX", f'{PROJECT_PATH}/hunt/presets/'
    )
    BOT_TOKEN: str = environ.get("BOT_TOKEN", "")
    ADMIN_TOKEN: str = environ.get("ADMIN_TOKEN", "")
    BOT_WEBHOOK_URL: str = environ.get("BOT_WEBHOOK_URL", "")
    BOT_PORT: str = environ.get("BOT_PORT", "")

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "user")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT"[-4:], 5432))
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "password")
    DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", 20)
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 15)

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for async connection with database
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    class Config:
        env_file = ".env"
