import os
from typing import List, Union

from pydantic import BaseSettings, validator

PROD = 'prod'
STAGING = 'staging'
DEV = 'dev'


class Settings(BaseSettings):
    """Catch App base Settings."""

    environment: str = None

    @validator('environment')
    def environment_values(cls, v):
        if v is None:
            return None
        if v not in [PROD, STAGING, DEV]:
            raise ValueError(f'Incorrect environment value: {v}')
        return v

    domain_name: str = 'localhost:5000'
    api_v1_path: str = '/api/v1'

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_directory = os.path.join(base_dir, 'media')

    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    DB_HOST = os.environ.get("DB_HOST")

    postgres_async_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    postgres_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

    SQLALCHEMY_DATABASE_URI = postgres_url

    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60 * 24 * 30

    access_token_secret_key = os.environ.get('ACCESS_TOKEN_SECRET')
    refresh_token_secret_key = os.environ.get('REFRESH_TOKEN_SECRET')

    backend_cors_origins: List[str] = ['*']

    @validator("backend_cors_origins", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[
        List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    project_name: str = 'Catch App'
    default_pagination_limit: int = 20


settings = Settings()

logging_conf = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        '': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'handlers': ['console', ],
            'propagate': True
        }
    }
}
