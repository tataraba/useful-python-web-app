from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import AnyUrl, BaseSettings, validator
from src.core.config import get_app_settings
from src.models.article import Article


settings = get_app_settings()

class DataBase(BaseSettings):
    """Utility class to define mongodb settings."""

    MONGO_DB_URI: Optional[AnyUrl] = None  # insert URI directly 

    @validator("MONGO_DB_URI", pre=True, check_fields=False)
    def db_is_valid(cls, v):
        if isinstance(v, AnyUrl):
            return v
        try:
            return AnyUrl.build(
                scheme=settings.MONGO_SCHEME,
                user=settings.MONGO_USER,
                password=settings.MONGO_PASS,
                host=settings.MONGO_HOST,
                path=f"/{settings.MONGO_DB}",
                query="retryWrites=true&w=majority"
            )
        except Exception:
            raise AttributeError(v)


async def initialize_db() -> None:
    """Initialize the database."""
    db = DataBase()  # create instance of DataBase
    
    auth_name = settings.MONGO_AUTH_NAME  # auth name used to log into mongo
    db_name = settings.MONGO_DB       # database name
    URI = f"{db.MONGO_DB_URI}/admin?authSource={auth_name}"
    
    try:
        await init_beanie(
            database=AsyncIOMotorClient(URI),   # create motor client with URI
            document_models=[Article]         # define document models
        )
    except Exception:
        raise ReferenceError("Database initialization failed.")


async def close_db() -> None:
    """Close the database."""
    db = DataBase()
    await db.client.close()