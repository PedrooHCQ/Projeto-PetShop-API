from sqlalchemy.orm import declarative_base

from pydantic_settings import BaseSettings

DBBaseModel = declarative_base()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/petshop"

    JWT_SECRET: str = "ea12e6eb4b6338254286d96a9f61857666a06bc16c01ad29b95cd5f3b4dcbe90"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()
