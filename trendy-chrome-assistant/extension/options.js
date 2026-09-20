import { loadState, saveState } from "./storage.js";
import { normalizeBaseUrl } from "./apiClient.js";

const form = document.querySelector("#optionsForm");
const apiBaseUrlInput = document.querySelector("#apiBaseUrl");
const lookbackInput = document.querySelector("#lookback");
const status = document.querySelector("#optionsStatus");

async function init() {
  const state = await loadState();
  apiBaseUrlInput.value = state.apiBaseUrl;
  lookbackInput.value = state.lookback;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const lookback = Number.parseInt(lookbackInput.value, 10);
  await saveState({
    apiBaseUrl: normalizeBaseUrl(apiBaseUrlInput.value),
    lookback: Number.isFinite(lookback) ? Math.min(Math.max(lookback, 60), 240) : 90
  });
  status.textContent = "Saved.";
  setTimeout(() => {
    status.textContent = "";
  }, 1800);
});

init();

