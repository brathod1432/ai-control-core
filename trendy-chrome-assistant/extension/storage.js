const DEFAULT_STATE = {
  apiBaseUrl: "http://127.0.0.1:8000",
  lastSymbol: "AAPL",
  lastTimeframe: "1d",
  lookback: 90,
  watchlist: ["AAPL", "MSFT", "NVDA"]
};

export async function loadState() {
  const stored = await chrome.storage.local.get(Object.keys(DEFAULT_STATE));
  return { ...DEFAULT_STATE, ...stored };
}

export async function saveState(patch) {
  await chrome.storage.local.set(patch);
}

export async function addWatchlistSymbol(symbol) {
  const state = await loadState();
  const normalized = normalizeSymbol(symbol);
  if (!normalized) {
    return state.watchlist;
  }

  const watchlist = [normalized, ...state.watchlist.filter((item) => item !== normalized)].slice(0, 12);
  await saveState({ watchlist });
  return watchlist;
}

export async function removeWatchlistSymbol(symbol) {
  const state = await loadState();
  const normalized = normalizeSymbol(symbol);
  const watchlist = state.watchlist.filter((item) => item !== normalized);
  await saveState({ watchlist });
  return watchlist;
}

export function normalizeSymbol(value) {
  return String(value || "")
    .trim()
    .toUpperCase()
    .replace(/[^A-Z0-9.\-^=]/g, "")
    .slice(0, 16);
}

