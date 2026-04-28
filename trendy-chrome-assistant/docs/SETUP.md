# Setup

## Backend

```powershell
cd trendy-chrome-assistant\backend
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Check the backend:

```powershell
curl http://127.0.0.1:8000/health
```

Run backend tests:

```powershell
pytest
```

## Extension

1. Open Chrome.
2. Go to `chrome://extensions`.
3. Enable Developer mode.
4. Click Load unpacked.
5. Select `trendy-chrome-assistant/extension`.
6. Pin the extension if desired.
7. Open the popup and click Analyze.
8. Open extension Options if you need to change the backend URL or default lookback.

## Notes

The starter backend uses deterministic sample data. It is designed this way so the project can run without external network calls, API keys, or account access.

## API Examples

```powershell
curl -X POST http://127.0.0.1:8000/analysis `
  -H "Content-Type: application/json" `
  -d "{\"symbol\":\"AAPL\",\"timeframe\":\"1d\",\"lookback\":90}"
```
