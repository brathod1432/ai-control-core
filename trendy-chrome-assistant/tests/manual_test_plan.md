# Manual Test Plan

## Backend Smoke Test

1. Start the backend with `uvicorn main:app --reload --port 8000`.
2. Visit `http://127.0.0.1:8000/health`.
3. Confirm the response is `{"status":"ok"}`.
4. Send a POST request to `/analysis` with:

```json
{
  "symbol": "AAPL",
  "timeframe": "1d",
  "lookback": 90
}
```

5. Confirm the response contains `signal`, `trend`, `momentum`, `confidence`, `indicators`, `price_points`, `summary`, and `risk_note`.

## Extension Smoke Test

1. Load `trendy-chrome-assistant/extension` through `chrome://extensions`.
2. Start the backend.
3. Open the extension popup.
4. Confirm the backend status dot turns green.
5. Enter `MSFT`.
6. Click Analyze.
7. Confirm the result updates without console errors.
8. Add `MSFT` to the watchlist.
9. Click the watchlist chip and confirm analysis runs again.
10. Open Options and confirm the backend URL and lookback can be saved.

## Safety Checks

1. Confirm the extension does not ask for broad browsing permissions.
2. Confirm no cookies are requested.
3. Confirm no password fields are read.
4. Confirm no orders or trade actions exist in the UI.
