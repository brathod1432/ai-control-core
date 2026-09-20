from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_provider_and_version() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["provider"] == "sample"
    assert body["version"]


def test_analyze_returns_expected_shape() -> None:
    response = client.post(
        "/analysis",
        json={"symbol": "AAPL", "timeframe": "1d", "lookback": 90},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "AAPL"
    assert body["provider"] == "sample"
    assert 0 <= body["confidence"] <= 100
    assert len(body["price_points"]) == 40
    assert body["risk_note"]


def test_batch_analysis_deduplicates_symbols() -> None:
    response = client.post(
        "/analysis/batch",
        json={"symbols": ["msft", "MSFT", "nvda"], "timeframe": "1wk", "lookback": 90},
    )

    assert response.status_code == 200
    body = response.json()
    assert [item["symbol"] for item in body["results"]] == ["MSFT", "NVDA"]


def test_invalid_symbol_is_rejected() -> None:
    response = client.post(
        "/analysis",
        json={"symbol": "<script>", "timeframe": "1d", "lookback": 90},
    )

    assert response.status_code == 422
