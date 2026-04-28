# Trendy Chrome Trading Assistant

Local-first Chrome extension and FastAPI backend for educational public-market technical analysis.

## What It Does

- Shows a compact Chrome popup for symbol analysis, watchlist checks, and current-tab symbol detection.
- Sends timeout-aware analysis requests to a local FastAPI backend at `http://127.0.0.1:8000`.
- Uses a pluggable backend market-data provider. The starter provider is deterministic sample data, so it runs without API keys or remote calls.
- Produces trend, momentum, confidence, indicator, sparkline, and risk notes.
- Avoids passwords, cookies, account access, scraping, and auto-trading.

## Project Structure

```text
trendy-chrome-assistant/
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── apiClient.js
│   ├── chart.js
│   ├── options.html
│   ├── options.js
│   ├── storage.js
│   ├── contentScript.js
│   ├── service_worker.js
│   ├── README.md
│   └── styles.css
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   ├── services/
│   │   └── providers/
│   ├── tests/
│   ├── .env.example
│   ├── main.py
│   ├── pyproject.toml
│   └── requirements.txt
├── docs/
│   ├── ROADMAP.md
│   ├── SETUP.md
│   └── SECURITY.md
└── tests/
    └── manual_test_plan.md
```

## Backend Setup

```powershell
cd trendy-chrome-assistant\backend
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend routes:

- `GET /health`
- `GET /config`
- `POST /analysis`
- `POST /analysis/batch`
- `POST /analyze` compatibility alias

## Chrome Extension Setup

1. Open Chrome.
2. Go to `chrome://extensions`.
3. Enable Developer mode.
4. Click Load unpacked.
5. Select `trendy-chrome-assistant/extension`.

## Safety Notes

This project is informational only. It does not trade, place orders, read brokerage pages, read credentials, read cookies, or scrape TradingView.

## Tests

```powershell
cd trendy-chrome-assistant\backend
pytest
```
