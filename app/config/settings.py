from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    WHATSAPP_API_KEY: str
    WHATSAPP_PHONE_NUMBER_ID: str
    REDIRECT_URI: str

    model_config = {"env_file": ".env"}


settings = Settings()
