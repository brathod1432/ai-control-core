from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import AnalysisRequest, AnalysisResponse
from app.routers import analysis, system
from app.services.providers import get_market_data_provider


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Local-first educational market analysis API.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://127.0.0.1"],
        allow_origin_regex=settings.cors_allow_origin_regex,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    app.include_router(system.router)
    app.include_router(analysis.router)
    _add_compat_routes(app)
    return app


def _add_compat_routes(app: FastAPI) -> None:
    @app.post("/analyze", response_model=AnalysisResponse)
    def analyze_compat(request: AnalysisRequest) -> AnalysisResponse:
        return analysis.analyze(request, get_market_data_provider())


app = create_app()
