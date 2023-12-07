# config.py - is used to handle environment variable
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


try:
    Settings(
        database_hostname="str",
        database_port="str",
        database_password="str",
        database_name="str",
        database_username="str",
        secret_key="str",
        algorithm="str",
        access_token_expire_minutes=1,
    )
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))

    # tell pydantic to connect with the file name
    model_config = SettingsConfigDict(env_file=".env")

    # class Config:
    #     env_file = ".env"


settings = Settings()
