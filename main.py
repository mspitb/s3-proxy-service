import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from src.api.routers.s3_api import router

from src.core.config.open_api import tags_metadata
from src.core.exceptions.exception_handler import ExceptionHandler

ENV_PROFILE = os.getenv("ENV_PROFILE", "dev")
if ENV_PROFILE == "dev":
    load_dotenv(".env.dev")
elif ENV_PROFILE == "test":
    load_dotenv(".env.test")

os.environ["ROOT_PATH"] = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="S3 Minio Proxy Service",
    descriptaion="API minio S3",
    version="1.0",
    openapi_tags=tags_metadata,
)

app.add_exception_handler(Exception, ExceptionHandler.handle)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=int(os.getenv("APP_PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info"),
        log_config="log_conf.yaml",
        reload=True,
    )
