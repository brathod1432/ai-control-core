chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    apiBaseUrl: "http://127.0.0.1:8000",
    lastSymbol: "AAPL",
    lastTimeframe: "1d",
    lookback: 90,
    watchlist: ["AAPL", "MSFT", "NVDA"]
  });
});
