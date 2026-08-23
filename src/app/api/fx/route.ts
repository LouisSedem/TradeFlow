import { NextResponse } from "next/server";
import { getUniqueCurrencies, getPapssCurrencies, getCrossRate } from "@/lib/currencies";

/** GET /api/fx — list supported currencies & rates */
export async function GET() {
  const all = getUniqueCurrencies();
  const papss = getPapssCurrencies();

  return NextResponse.json({
    currencies: all.map((c) => ({
      code: c.code,
      name: c.name,
      symbol: c.symbol,
      flag: c.flag,
      country: c.country,
      countryAlpha2: c.countryAlpha2,
      rateToUSD: c.rateToUSD,
      papssLive: c.papssLive,
      afcftaMember: c.afcftaMember,
    })),
    papssCurrencyCodes: papss.map((c) => c.code),
  });
}
