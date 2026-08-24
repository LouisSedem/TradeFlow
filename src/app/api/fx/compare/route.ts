import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { compareMethods, calculateSavings, type DeliveryMethodFilter } from "@/lib/fx-engine";
import { getCurrency, getCrossRate } from "@/lib/currencies";
import { getLiveRates } from "@/lib/fx-rates";
import { db } from "@/lib/db";

const CompareSchema = z.object({
  sendCurrency: z.string().length(3),
  receiveCurrency: z.string().length(3),
  sendAmount: z.number().positive().max(10_000_000),
  deliveryMethod: z.enum(["bank_deposit", "mobile_money", "cash_pickup", "all"]).optional().default("all"),
});

/** POST /api/fx/compare — compare payment methods for a transfer */
export async function POST(request: NextRequest) {
  const body = await request.json();
  const parsed = CompareSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: "Invalid request", details: parsed.error.flatten() },
      { status: 400 }
    );
  }

  const { sendCurrency, receiveCurrency, sendAmount, deliveryMethod } = parsed.data;

  // Validate currencies exist
  const sendCur = getCurrency(sendCurrency);
  const recvCur = getCurrency(receiveCurrency);
  if (!sendCur || !recvCur) {
    return NextResponse.json(
      { error: "Unsupported currency" },
      { status: 400 }
    );
  }

  // Fetch live rates
  const { rates: liveRates, source: rateSource, fetchedAt: rateFetchedAt } = await getLiveRates();

  // Run comparison
  const results = compareMethods(sendCurrency, receiveCurrency, sendAmount, {
    deliveryMethod: deliveryMethod as DeliveryMethodFilter,
    liveRates,
  });
  const savings = calculateSavings(results);

  // Mid-market rate using live rates
  const midMarketRate = getCrossRate(sendCurrency, receiveCurrency, liveRates);

  // Log comparison (anonymous — no auth required for Phase 1)
  try {
    const ip = request.headers.get("x-forwarded-for") || request.headers.get("x-real-ip") || "unknown";
    const ua = request.headers.get("user-agent") || "unknown";
    await db.comparisonLog.create({
      data: {
        sendCurrency,
        receiveCurrency,
        sendAmount,
        ipAddress: ip.slice(0, 45),
        userAgent: ua.slice(0, 200),
      },
    });
  } catch {
    // Logging failure shouldn't block the response
  }

  return NextResponse.json({
    sendCurrency,
    receiveCurrency,
    sendAmount,
    midMarketRate,
    sendCurrencyInfo: { code: sendCur.code, symbol: sendCur.symbol, flag: sendCur.flag, name: sendCur.name },
    receiveCurrencyInfo: { code: recvCur.code, symbol: recvCur.symbol, flag: recvCur.flag, name: recvCur.name },
    methods: results,
    savings,
    rateSource,
    rateFetchedAt: rateFetchedAt?.toISOString() || null,
  });
}
