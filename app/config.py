from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: Optional[str] = "localhost"
    database_port: Optional[str] = "5432"
    database_password: Optional[str] = "postgres"
    database_name: Optional[str] = "rentsphere"
    database_username: Optional[str] = "postgres"
    database_url: Optional[str] = None
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
