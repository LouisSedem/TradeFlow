/**
 * Live FX rate fetching module with fallback chain.
 * Tries free APIs in priority order, falls back to hardcoded rates.
 */

export interface LiveRatesResult {
  rates: Map<string, number>; // currency code → 1 unit = ? USD
  source: string;
  fetchedAt: Date | null;
}

interface CachedRates {
  rates: Map<string, number>;
  source: string;
  fetchedAt: Date;
}

const CACHE_TTL_MS = 60_000; // 60 seconds
let cachedRates: CachedRates | null = null;

/** Supported currency codes */
const SUPPORTED_CODES = new Set([
  // West Africa
  "GHS", "NGN", "XOF",
  // East Africa
  "KES", "TZS", "UGX", "RWF", "ETB",
  // Southern Africa
  "ZAR", "BWP", "NAD", "MWK", "ZMW",
  // North Africa
  "EGP", "MAD", "TND",
  // Central Africa
  "XAF", "CDF",
  // Major
  "USD", "EUR", "GBP",
]);

/** Hardcoded fallback rates (1 unit = ? USD) */
function getHardcodedRates(): Map<string, number> {
  const map = new Map<string, number>([
    ["GHS", 0.0647], ["NGN", 0.000635], ["XOF", 0.00164],
    ["KES", 0.00772], ["TZS", 0.000383], ["UGX", 0.000271], ["RWF", 0.000773], ["ETB", 0.00813],
    ["ZAR", 0.0544], ["BWP", 0.0741], ["NAD", 0.0544], ["MWK", 0.000576], ["ZMW", 0.0362],
    ["EGP", 0.0202], ["MAD", 0.100], ["TND", 0.316],
    ["XAF", 0.00164], ["CDF", 0.000352],
    ["USD", 1.0], ["EUR", 1.085], ["GBP", 1.27],
  ]);
  return map;
}

/** Fetch from exchangerate-api.com (free, no key) */
async function fetchFromExchangeRateAPI(): Promise<Map<string, number> | null> {
  try {
    const res = await fetch("https://api.exchangerate-api.com/v4/latest/USD", {
      signal: AbortSignal.timeout(5000),
    });
    if (!res.ok) return null;
    const data = await res.json();
    // This API returns { rates: { "GHS": 15.45, ... } } meaning 1 USD = X GHS
    // We need 1 GHS = ? USD, so we invert
    const usdRates = data.rates as Record<string, number>;
    const inverted = new Map<string, number>();
    for (const code of SUPPORTED_CODES) {
      if (code === "USD") {
        inverted.set("USD", 1.0);
      } else if (usdRates[code] && usdRates[code] > 0) {
        inverted.set(code, 1 / usdRates[code]);
      }
    }
    return inverted;
  } catch {
    return null;
  }
}

/** Fetch from open.er-api.com (free fallback) */
async function fetchFromOpenERAPI(): Promise<Map<string, number> | null> {
  try {
    const res = await fetch("https://open.er-api.com/v6/latest/USD", {
      signal: AbortSignal.timeout(5000),
    });
    if (!res.ok) return null;
    const data = await res.json();
    const usdRates = data.rates as Record<string, number>;
    const inverted = new Map<string, number>();
    for (const code of SUPPORTED_CODES) {
      if (code === "USD") {
        inverted.set("USD", 1.0);
      } else if (usdRates[code] && usdRates[code] > 0) {
        inverted.set(code, 1 / usdRates[code]);
      }
    }
    return inverted;
  } catch {
    return null;
  }
}

/**
 * Fetch live rates with fallback chain.
 * 1. Check cache (60s TTL)
 * 2. Try exchangerate-api.com
 * 3. Try open.er-api.com
 * 4. Fall back to hardcoded rates
 */
export async function getLiveRates(): Promise<LiveRatesResult> {
  // Return cached if still valid
  if (cachedRates && Date.now() - cachedRates.fetchedAt.getTime() < CACHE_TTL_MS) {
    return {
      rates: cachedRates.rates,
      source: cachedRates.source,
      fetchedAt: cachedRates.fetchedAt,
    };
  }

  // Try API sources
  const fromAPI1 = await fetchFromExchangeRateAPI();
  if (fromAPI1 && fromAPI1.size > 0) {
    const now = new Date();
    cachedRates = { rates: fromAPI1, source: "ExchangeRate-API (live)", fetchedAt: now };
    return { rates: fromAPI1, source: cachedRates.source, fetchedAt: now };
  }

  const fromAPI2 = await fetchFromOpenERAPI();
  if (fromAPI2 && fromAPI2.size > 0) {
    const now = new Date();
    cachedRates = { rates: fromAPI2, source: "Open ER API (live)", fetchedAt: now };
    return { rates: fromAPI2, source: cachedRates.source, fetchedAt: now };
  }

  // Fallback to hardcoded
  const hardcoded = getHardcodedRates();
  return {
    rates: hardcoded,
    source: "Hardcoded estimates",
    fetchedAt: null,
  };
}
