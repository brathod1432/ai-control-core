from fastapi import APIRouter

from app.config import get_settings
from app.models import AppConfigResponse, HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", version=settings.app_version, provider=settings.data_provider)


@router.get("/config", response_model=AppConfigResponse)
def config() -> AppConfigResponse:
    settings = get_settings()
    return AppConfigResponse(
        app_name=settings.app_name,
        app_version=settings.app_version,
        data_provider=settings.data_provider,
        supported_timeframes=["1d", "1wk", "1mo"],
    )

