import os
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Bank Account Service")
    app_env: str = os.getenv("APP_ENV", "production")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./bank_production.db")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
