from pydantic_settings import BaseSettings
from dotenv import find_dotenv
from typing import ClassVar

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config(BaseSettings):
        env_file: ClassVar[str]  = find_dotenv(".env")
        # env_file = ".env" #this does not work

settings = Settings()