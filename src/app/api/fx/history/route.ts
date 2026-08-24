import { NextRequest, NextResponse } from "next/server";

interface HistoryPoint {
  date: string;
  rate: number;
}

const HISTORY_CACHE = new Map<string, { data: HistoryPoint[]; fetchedAt: number }>();
const CACHE_TTL = 30 * 60 * 1000; // 30 min cache

/**
 * GET /api/fx/history?send=GHS&receive=KES&days=30
 * Fetches real historical FX data from ExchangeRate-API.
 * Falls back to simulated data if the API fails.
 */
export async function GET(req: NextRequest) {
  const url = new URL(req.url);
  const send = url.searchParams.get("send")?.toUpperCase();
  const receive = url.searchParams.get("receive")?.toUpperCase();
  const days = Math.min(Math.max(parseInt(url.searchParams.get("days") || "30"), 7), 90);

  if (!send || !receive || send === receive) {
    return NextResponse.json({ error: "Provide different send and receive currencies" }, { status: 400 });
  }

  const cacheKey = `${send}-${receive}-${days}`;
  const cached = HISTORY_CACHE.get(cacheKey);
  if (cached && Date.now() - cached.fetchedAt < CACHE_TTL) {
    return NextResponse.json({ data: cached.data, source: "cached" });
  }

  // Try real history from ExchangeRate-API
  try {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days + 1);
    const startStr = startDate.toISOString().split("T")[0];
    const endStr = endDate.toISOString().split("T")[0];

    const res = await fetch(
      `https://api.exchangerate-api.com/v4/history/${send}?start_date=${startStr}&end_date=${endStr}&currencies=${receive}`,
      { signal: AbortSignal.timeout(8000) }
    );

    if (res.ok) {
      const json = await res.json();
      const ratesByDate: Record<string, Record<string, number>> = json.rates || {};
      const points: HistoryPoint[] = [];
      const dates = Object.keys(ratesByDate).sort();
      for (const date of dates) {
        const rate = ratesByDate[date][receive];
        if (rate && rate > 0) {
          points.push({ date, rate });
        }
      }

      if (points.length >= Math.floor(days * 0.5)) {
        HISTORY_CACHE.set(cacheKey, { data: points, fetchedAt: Date.now() });
        return NextResponse.json({ data: points, source: "ExchangeRate-API (live)" });
      }
    }
  } catch {
    // fall through
  }

  // Fallback: simulated data
  const fallbackData = generateSimulated(currentRate, days);
  HISTORY_CACHE.set(cacheKey, { data: fallbackData, fetchedAt: Date.now() });
  return NextResponse.json({ data: fallbackData, source: "Simulated (API unavailable)" });
}

function currentRate(): number {
  // Will be overridden by the query context; this is just for the fallback path
  return 1.0;
}

function generateSimulated(baseRate: number, days: number): HistoryPoint[] {
  const points: HistoryPoint[] = [];
  const seed = Math.round(baseRate * 10000);
  let rng = seed;
  const prng = () => { rng = (rng * 16807) % 2147483647; return (rng - 1) / 2147483646; };
  const vol = baseRate > 100 ? 0.015 : baseRate > 10 ? 0.01 : 0.005;
  const rates: number[] = [baseRate];
  for (let i = 1; i < days; i++) {
    const change = (prng() - 0.5) * 2 * vol;
    rates.unshift(Math.max(rates[0] / (1 + change), baseRate * 0.85));
  }
  const today = new Date();
  for (let i = 0; i < days; i++) {
    const d = new Date(today);
    d.setDate(d.getDate() - (days - 1 - i));
    points.push({ date: d.toISOString().split("T")[0], rate: Math.round(rates[i] * 100000) / 100000 });
  }
  return points;
}
