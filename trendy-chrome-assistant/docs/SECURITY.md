# Security

## Baseline

- No password reading.
- No cookie reading.
- No brokerage account access.
- No automatic trading.
- No TradingView scraping.
- No remote telemetry.
- No analytics SDK.

## Extension Permissions

The extension requests only:

- `storage` for saving the last symbol and timeframe locally.
- `activeTab` for asking supported active tabs for title and URL context when the user clicks the detect button.
- local backend host permissions for `http://127.0.0.1/*` and `http://localhost/*`.

The content script only returns page title, URL, and host when explicitly messaged by the extension.

## Backend

The backend starts with generated sample market data. When a real market-data provider is added, prefer official APIs, local environment variables for credentials, timeouts, and clear provider error handling. Do not add telemetry, analytics, or background uploads.

## Trading Disclaimer

The assistant is educational and informational. It must not place trades, manage orders, or make promises about returns.
