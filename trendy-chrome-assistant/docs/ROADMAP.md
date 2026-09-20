# Roadmap

## Phase 1: Local Starter

- Chrome extension popup.
- Local FastAPI backend.
- Deterministic sample data.
- Trend, momentum, RSI, ATR, moving averages, confidence, and sparkline data.
- Watchlist and options page.
- Manual install and smoke test instructions.

## Phase 2: Real Public Data

- Add a maintained public market data provider.
- Keep API keys, if any, in local environment variables.
- Add provider timeout and error handling.
- Add backend unit tests for data-provider failures.
- Add explicit provider-selection docs before any real network provider is enabled.

## Phase 3: Better Analysis

- Add support/resistance and richer volume context.
- Add confidence scoring with transparent inputs.
- Add exportable local notes.

## Phase 4: Hardening

- Add automated backend tests.
- Add extension linting.
- Add request rate limiting.
- Add local configuration for allowed origins.
