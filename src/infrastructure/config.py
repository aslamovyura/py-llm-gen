from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    api_title: str = "DB Search API"
    api_description: str = "API for searching deals in the database"
    api_version: str = "1.0.0"
    debug: bool = False

    # Database Settings
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/deals"
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # Search Settings
    min_search_chars: int = 3
    max_search_results: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings with caching.
    """
    return Settings() 