
from pathlib import Path
from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = PROJECT_ROOT / ".env"


settings = Settings()
