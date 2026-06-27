from fastapi import FastAPI
from contextlib import asynccontextmanager
from middlewares.cors import apply_cors_middleware
from routers import api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app = apply_cors_middleware(app)
    app.include_router(api_router)
    return app