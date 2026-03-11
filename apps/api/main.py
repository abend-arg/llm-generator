import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.router import router

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    app = FastAPI()
    cors_env = os.getenv("CORS_ORIGINS", "")
    cors_origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    app.include_router(router)
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
