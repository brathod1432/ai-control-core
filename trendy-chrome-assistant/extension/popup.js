import { ApiClient } from "./apiClient.js";
import { drawSparkline } from "./chart.js";
import { addWatchlistSymbol, loadState, normalizeSymbol, removeWatchlistSymbol, saveState } from "./storage.js";

const form = document.querySelector("#analysisForm");
const result = document.querySelector("#result");
const statusDot = document.querySelector("#statusDot");
const analyzeButton = document.querySelector("#analyzeButton");
const detectButton = document.querySelector("#detectButton");
const addWatchlistButton = document.querySelector("#addWatchlistButton");
const symbolInput = document.querySelector("#symbol");
const timeframeInput = document.querySelector("#timeframe");
const lookbackInput = document.querySelector("#lookback");
const watchlist = document.querySelector("#watchlist");
const sparkline = document.querySelector("#sparkline");

let client = new ApiClient("http://127.0.0.1:8000");
let currentState = null;

async function checkHealth() {
  try {
    const response = await client.health();
    statusDot.classList.add("online");
    statusDot.title = `Backend online (${response.provider})`;
  } catch {
    statusDot.classList.remove("online");
    statusDot.title = "Backend offline";
  }
}

function renderLoading() {
  result.innerHTML = `<p class="muted">Analyzing market data locally...</p>`;
}

function renderError(message) {
  result.innerHTML = `<p class="error">${escapeHtml(message)}</p>`;
}

function renderAnalysis(payload) {
  result.innerHTML = `
    <div class="metric-row">
      <span>Last</span>
      <strong>${escapeHtml(payload.last_close.toFixed(2))} (${escapeHtml(payload.change_percent.toFixed(2))}%)</strong>
    </div>
    <div class="metric-row">
      <span>Signal</span>
      <strong>${escapeHtml(payload.signal)}</strong>
    </div>
    <div class="metric-row">
      <span>Trend</span>
      <strong>${escapeHtml(payload.trend)}</strong>
    </div>
    <div class="metric-row">
      <span>Momentum</span>
      <strong>${escapeHtml(payload.momentum)}</strong>
    </div>
    <div class="metric-row">
      <span>Confidence</span>
      <strong>${escapeHtml(payload.confidence)}%</strong>
    </div>
    <p>${escapeHtml(payload.summary)}</p>
    <p class="muted">${escapeHtml(payload.risk_note)}</p>
  `;

  drawSparkline(sparkline, payload.price_points || []);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function analyze(event) {
  event?.preventDefault();

  const symbol = normalizeSymbol(symbolInput.value);
  const timeframe = timeframeInput.value;
  const lookback = Number.parseInt(lookbackInput.value, 10) || currentState?.lookback || 90;

  if (!symbol) {
    renderError("Enter a symbol first.");
    return;
  }

  analyzeButton.disabled = true;
  renderLoading();

  try {
    await saveState({ lastSymbol: symbol, lastTimeframe: timeframe, lookback });
    renderAnalysis(await client.analyze({ symbol, timeframe, lookback }));
    statusDot.classList.add("online");
  } catch (error) {
    statusDot.classList.remove("online");
    renderError(error.message || "Analysis failed. Is the backend running?");
  } finally {
    analyzeButton.disabled = false;
  }
}

async function restoreState() {
  currentState = await loadState();
  client = new ApiClient(currentState.apiBaseUrl);
  symbolInput.value = currentState.lastSymbol;
  timeframeInput.value = currentState.lastTimeframe;
  lookbackInput.value = currentState.lookback;
  renderWatchlist(currentState.watchlist);
}

function renderWatchlist(items) {
  if (!items.length) {
    watchlist.innerHTML = `<p class="muted">No symbols saved yet.</p>`;
    return;
  }

  watchlist.innerHTML = items.map((item) => `
    <button class="watch-chip" type="button" data-symbol="${escapeHtml(item)}">
      <span>${escapeHtml(item)}</span>
      <span class="remove" data-remove="${escapeHtml(item)}">x</span>
    </button>
  `).join("");
}

async function detectSymbolFromCurrentTab() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) {
      throw new Error("No active tab found.");
    }

    const response = await chrome.tabs.sendMessage(tab.id, { type: "GET_PAGE_CONTEXT" });
    const detected = extractSymbol(response?.url || "", response?.title || "");
    if (!detected) {
      throw new Error("No symbol found on this page.");
    }

    symbolInput.value = detected;
  } catch (error) {
    renderError(error.message || "Could not detect a symbol from this tab.");
  }
}

function extractSymbol(url, title) {
  const candidates = [
    /symbol=([A-Za-z0-9.\-^=]+)/i.exec(url)?.[1],
    /\/quote\/([A-Za-z0-9.\-^=]+)/i.exec(url)?.[1],
    /^([A-Za-z0-9.\-^=]{1,16})\s/.exec(title)?.[1]
  ];
  return normalizeSymbol(candidates.find(Boolean));
}

form.addEventListener("submit", analyze);
detectButton.addEventListener("click", detectSymbolFromCurrentTab);
addWatchlistButton.addEventListener("click", async () => {
  renderWatchlist(await addWatchlistSymbol(symbolInput.value));
});
watchlist.addEventListener("click", async (event) => {
  const removeSymbol = event.target.dataset.remove;
  if (removeSymbol) {
    event.stopPropagation();
    renderWatchlist(await removeWatchlistSymbol(removeSymbol));
    return;
  }

  const chip = event.target.closest("[data-symbol]");
  if (chip) {
    symbolInput.value = chip.dataset.symbol;
    await analyze();
  }
});

restoreState().then(checkHealth);
