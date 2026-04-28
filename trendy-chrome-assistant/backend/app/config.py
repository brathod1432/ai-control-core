from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TRENDY_", env_file=".env", extra="ignore")

    app_name: str = "Trendy Trading Assistant API"
    app_version: str = "0.1.0"
    data_provider: str = "sample"
    cors_allow_origin_regex: str = r"^chrome-extension://[a-zA-Z0-9]+$"


class PublicSettings(BaseModel):
    app_name: str
    app_version: str
    data_provider: str


@lru_cache
def get_settings() -> Settings:
    return Settings()

