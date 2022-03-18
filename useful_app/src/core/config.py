from typing import Optional, Dict, Any, Union
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, BaseSettings, Field


APP_DIRECTORY = Path(__file__).parent.parent
print(APP_DIRECTORY)

class AppConfig(BaseModel):
    """Application configuration using pydantic `BaseModel`. 
    Will be accessed as `more_settings` within the application.
    """

    title: str = "App4Realz"
    version: str = "0.1.0"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"


class GlobalConfig(BaseSettings):
    """Global configuration using pydantic `BaseSettings`.
    Will be accessed as `settings` within the application.
    """

    more_settings: AppConfig = AppConfig()
    APP_DIR: Path = APP_DIRECTORY
    

    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")
    DISABLE_DOCS: bool = False

    SECRET_KEY: str = "overriden_by_dotenv_value"

    MONGO_SCHEME: Optional[str] = None
    MONGO_HOST: Optional[str] = None
    MONGO_PORT: Optional[str] = None
    MONGO_USER: Optional[str] = None
    MONGO_PASS: Optional[str] = None
    MONGO_DB: Optional[str] = None

    @property   # Optional - makes loading values to FastAPI easier
    def fastapi_kwargs(self) -> Dict[str, str]:
        fastapi_kwargs = self.more_settings.dict()
        if self.DISABLE_DOCS:     # Disable FastAPI docs when in prd
            fastapi_kwargs.update(
                {
                    "docs_url": None,
                    "redoc_url": None,
                    "openapi_url": None,
                    "openapi_prefix": None,
                }
            )
        return fastapi_kwargs

    class Config:
        env_file = APP_DIRECTORY.parent / ".env"
        env_file_encoding = "utf-8"

class DevConfig(GlobalConfig):
    """Configuration for development environment.
    """

    class Config:
        env_prefix = "DEV_"


class PrdConfig(GlobalConfig):
    """Configuration for production environment.
    """

    class Config:
        env_prefix = "PRD_"



class FactoryConfig:
    """Callable class. Will load `DevConfig` or `PrdConfig`
    depending on the `ENV_STATE` set in the `GlobalConfig`
    class.
    """

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self) -> Any:
        if self.env_state == "dev":

            return DevConfig()

        elif self.env_state == "prd":
            return PrdConfig()


settings = FactoryConfig(GlobalConfig().ENV_STATE)()


@lru_cache()
def get_app_settings() -> Union[DevConfig, PrdConfig]:
    """Returns a cached instance of the settings (config) object.
    To change env variable and reset cache during 
    testing, use the 'lru_cache' instance method 
    'get_app_settings.cache_clear()'.
    """

    return settings

print(settings.__repr__())