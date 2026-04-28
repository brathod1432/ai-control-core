from fastapi import APIRouter, Depends, HTTPException

from app.domain import MarketDataError
from app.models import AnalysisRequest, AnalysisResponse, BatchAnalysisRequest, BatchAnalysisResponse
from app.providers.base import MarketDataProvider
from app.services.analyzer import analyze_market_data
from app.services.providers import get_market_data_provider

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalysisResponse)
def analyze(
    request: AnalysisRequest,
    provider: MarketDataProvider = Depends(get_market_data_provider),
) -> AnalysisResponse:
    try:
        bars = provider.fetch(request.symbol, request.timeframe, request.lookback)
    except MarketDataError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return analyze_market_data(request, bars, provider.name)


@router.post("/batch", response_model=BatchAnalysisResponse)
def analyze_batch(
    request: BatchAnalysisRequest,
    provider: MarketDataProvider = Depends(get_market_data_provider),
) -> BatchAnalysisResponse:
    results: list[AnalysisResponse] = []
    for symbol in request.symbols:
        analysis_request = AnalysisRequest(symbol=symbol, timeframe=request.timeframe, lookback=request.lookback)
        try:
            bars = provider.fetch(analysis_request.symbol, analysis_request.timeframe, analysis_request.lookback)
        except MarketDataError as exc:
            raise HTTPException(status_code=502, detail=f"{symbol}: {exc}") from exc
        results.append(analyze_market_data(analysis_request, bars, provider.name))

    return BatchAnalysisResponse(results=results)

