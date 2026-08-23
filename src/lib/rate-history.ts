/**
 * Generate realistic 30-day simulated historical data for any currency pair.
 * Uses the current rate as the latest point and applies realistic daily volatility.
 */

export interface RateHistoryPoint {
  date: string;
  rate: number;
}

/**
 * Generate 30 days of simulated rate history.
 * African currencies typically have 0.3-2% daily volatility.
 */
export function generateRateHistory(currentRate: number, days: number = 30): RateHistoryPoint[] {
  const points: RateHistoryPoint[] = [];
  let rate = currentRate;

  // Walk backwards from today using a seeded random walk
  // Use a deterministic seed based on the current rate so it's stable
  const seed = Math.round(currentRate * 10000);
  let rng = seed;
  const pseudoRandom = () => {
    rng = (rng * 16807 + 0) % 2147483647;
    return (rng - 1) / 2147483646;
  };

  // Determine volatility based on rate magnitude (African FX rates)
  // Higher rates (many units per USD) tend to be more volatile
  const dailyVolatility = rate > 100 ? 0.015 : rate > 10 ? 0.01 : rate > 1 ? 0.005 : 0.003;

  // Generate data backwards so the last point matches current rate
  const rates: number[] = [currentRate];
  for (let i = 1; i < days; i++) {
    const change = (pseudoRandom() - 0.5) * 2 * dailyVolatility;
    const prevRate = rates[rates.length - 1] / (1 + change);
    rates.unshift(Math.max(prevRate, currentRate * 0.85)); // floor at 85% of current
  }

  const today = new Date();
  for (let i = 0; i < days; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() - (days - 1 - i));
    points.push({
      date: date.toISOString().split("T")[0],
      rate: Math.round(rates[i] * 100000) / 100000,
    });
  }

  return points;
}

/** Get stats from rate history */
export function getRateStats(history: RateHistoryPoint[]) {
  const rates = history.map((h) => h.rate);
  const min = Math.min(...rates);
  const max = Math.max(...rates);
  return {
    min: Math.round(min * 100000) / 100000,
    max: Math.round(max * 100000) / 100000,
    range: Math.round((max - min) * 100000) / 100000,
    avg: Math.round((rates.reduce((a, b) => a + b, 0) / rates.length) * 100000) / 100000,
    trend: rates[rates.length - 1] > rates[0] ? "up" : rates[rates.length - 1] < rates[0] ? "down" : "flat",
  };
}
