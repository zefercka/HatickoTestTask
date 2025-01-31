import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_BOT_HOST: str
    DB_BOT_PORT: int
    DB_BOT_NAME: str
    DB_BOT_USER: str
    DB_BOT_PASSWORD: str
    TELEGRAM_TOKEN: str
    ADMIN_ID: int
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )
    

class Constants:
    BASE_API_URL = 'http://127.0.0.1:8000/api'
    IMEI_API_ROUTE = '/imei'
    
    LEVEL_TO_ADD = 5
    
    ID_PER_PAGE = 50
    

settings = Settings()
constants = Constants()

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_BOT_USER}:{settings.DB_BOT_PASSWORD}@"
            f"{settings.DB_BOT_HOST}:{settings.DB_BOT_PORT}/{settings.DB_BOT_NAME}")