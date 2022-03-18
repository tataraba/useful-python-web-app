from fastapi import FastAPI
from src.core.config import get_app_settings

def get_app() -> FastAPI:

    get_app_settings.cache_clear()
    settings = get_app_settings()
    print(settings)

    app = FastAPI(**settings.fastapi_kwargs)

    return app


app = get_app()