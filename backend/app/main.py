from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.sentry import init_sentry

setup_logging(settings.LOG_LEVEL)
init_sentry()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
    }
