# Chrome Extension

This is a Manifest V3 extension. It talks only to the local backend URL saved in extension storage, defaulting to `http://127.0.0.1:8000`.

## Files

- `manifest.json`: extension manifest, permissions, popup, options page, and content script registration.
- `popup.html`: assistant popup UI.
- `popup.js`: popup workflow and event handling.
- `apiClient.js`: timeout-aware backend client.
- `storage.js`: Chrome local storage helpers.
- `chart.js`: canvas sparkline rendering.
- `contentScript.js`: passive page context provider for supported finance pages.
- `options.html` / `options.js`: local backend URL and lookback settings.
- `styles.css`: popup and options styling.

## Load Locally

1. Open `chrome://extensions`.
2. Enable Developer mode.
3. Click Load unpacked.
4. Select this `extension` directory.

## Permissions

- `storage`: saves local settings and watchlist.
- `activeTab`: lets the popup ask the active supported tab for lightweight page context.
- host permissions for local HTTP backends on `127.0.0.1` and `localhost`.
