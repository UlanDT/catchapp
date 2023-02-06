from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from core.settings import settings, logging_conf
from api.api_v1.api import api_router

dictConfig(logging_conf)

openapi_url = f'{settings.api_v1_path}/openapi.json'

app = FastAPI(
    title=settings.project_name, openapi_url=openapi_url
)

app.include_router(api_router, prefix=settings.api_v1_path)

# Set all CORS enabled origins
if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.project_name,
        version='0.1.0',
        description='CatchApp API',
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
