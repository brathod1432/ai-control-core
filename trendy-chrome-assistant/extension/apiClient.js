export class ApiClient {
  constructor(baseUrl, timeoutMs = 8000) {
    this.baseUrl = normalizeBaseUrl(baseUrl);
    this.timeoutMs = timeoutMs;
  }

  async health() {
    return this.#request("/health", { method: "GET" });
  }

  async analyze({ symbol, timeframe, lookback }) {
    return this.#request("/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbol, timeframe, lookback })
    });
  }

  async analyzeBatch({ symbols, timeframe, lookback }) {
    return this.#request("/analysis/batch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbols, timeframe, lookback })
    });
  }

  async #request(path, init) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(`${this.baseUrl}${path}`, {
        ...init,
        signal: controller.signal
      });

      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload.detail || `Backend returned HTTP ${response.status}`);
      }

      return payload;
    } catch (error) {
      if (error.name === "AbortError") {
        throw new Error("Backend request timed out.");
      }
      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }
}

export function normalizeBaseUrl(value) {
  const trimmed = String(value || "").trim().replace(/\/+$/, "");
  return trimmed || "http://127.0.0.1:8000";
}

