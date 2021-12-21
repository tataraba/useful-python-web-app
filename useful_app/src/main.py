from fastapi import FastAPI

def get_app() -> FastAPI:

    app = FastAPI()

    return app


app = get_app()