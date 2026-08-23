/**
 * FX Engine — payment method comparison logic.
 * Compares PAPSS vs traditional cross-border payment methods.
 */

import { getCrossRate, type Currency } from "./currencies";

export interface PaymentMethodResult {
  method: string;
  methodType: "papss" | "bank" | "mto" | "fintech";
  recipientGets: number;
  totalFee: number;
  totalFeePercent: number;
  exchangeRate: number;
  exchangeRateMarkup: number;
  speed: string;
  speedRank: number; // 1 = fastest
  reliability: string;
  colorClass: string; // for UI theming
  deliveryMethod: string; // delivery method category
}

export type DeliveryMethodFilter = "bank_deposit" | "mobile_money" | "cash_pickup" | "all";

interface PaymentMethodConfig {
  name: string;
  type: "papss" | "bank" | "mto" | "fintech";
  deliveryMethod: "bank_deposit" | "mobile_money" | "cash_pickup";
  fxMarkupPercent: number; // markup on mid-market rate
  flatFeePercent: number;  // percentage fee on amount
  flatFeeMin: number;     // minimum flat fee in send currency
  flatFeeMax: number;     // maximum flat fee
  speed: string;
  speedRank: number;
  reliability: string;
  colorClass: string;
}

/**
 * Payment method configurations based on real-world data.
 * Sources: Afreximbank PAPSS fee structure, World Bank Remittance Prices
 * Worldwide database, commercial bank fee schedules.
 *
 * PAPSS fees:
 *   - Afreximbank clearing: ~0.125%
 *   - Sending bank: 0.1-0.5%
 *   - No FX markup (uses near mid-market rate)
 *   - Total typical: 0.25-0.5%
 *
 * SWIFT/Bank Transfer:
 *   - Correspondent bank fees: $15-50 flat
 *   - FX markup: 1.5-3%
 *   - Sending bank fee: 0.5-1.5%
 *   - Total typical: 2-5%
 *
 * MTO (Western Union, MoneyGram):
 *   - Transfer fee: 2-8% depending on corridor
 *   - FX markup: 3-7%
 *   - Total typical: 5-12%
 */
const PAYMENT_METHODS: PaymentMethodConfig[] = [
  {
    name: "PAPSS",
    type: "papss",
    deliveryMethod: "bank_deposit",
    fxMarkupPercent: 0.15,   // minimal FX markup
    flatFeePercent: 0.25,     // Afreximbank + bank processing
    flatFeeMin: 2,
    flatFeeMax: 200,
    speed: "Instant",
    speedRank: 1,
    reliability: "High",
    colorClass: "emerald",
  },
  {
    name: "Bank Transfer (SWIFT)",
    type: "bank",
    deliveryMethod: "bank_deposit",
    fxMarkupPercent: 2.0,
    flatFeePercent: 1.0,
    flatFeeMin: 10,
    flatFeeMax: 500,
    speed: "2-5 days",
    speedRank: 4,
    reliability: "High",
    colorClass: "slate",
  },
  {
    name: "Mobile Money",
    type: "fintech",
    deliveryMethod: "mobile_money",
    fxMarkupPercent: 1.5,
    flatFeePercent: 1.5,
    flatFeeMin: 1,
    flatFeeMax: 100,
    speed: "Instant",
    speedRank: 2,
    reliability: "Medium",
    colorClass: "amber",
  },
  {
    name: "Western Union",
    type: "mto",
    deliveryMethod: "cash_pickup",
    fxMarkupPercent: 4.0,
    flatFeePercent: 3.5,
    flatFeeMin: 5,
    flatFeeMax: 1000,
    speed: "Minutes",
    speedRank: 2,
    reliability: "High",
    colorClass: "yellow",
  },
  {
    name: "MoneyGram",
    type: "mto",
    deliveryMethod: "cash_pickup",
    fxMarkupPercent: 3.5,
    flatFeePercent: 3.0,
    flatFeeMin: 5,
    flatFeeMax: 800,
    speed: "Minutes",
    speedRank: 2,
    reliability: "High",
    colorClass: "orange",
  },
];

/**
 * Compare payment methods for a given send/receive pair.
 */
export function compareMethods(
  sendCurrencyCode: string,
  receiveCurrencyCode: string,
  sendAmount: number,
  options?: {
    deliveryMethod?: DeliveryMethodFilter;
    liveRates?: Map<string, number>;
  }
): PaymentMethodResult[] {
  const midMarketRate = getCrossRate(sendCurrencyCode, receiveCurrencyCode, options?.liveRates);

  if (midMarketRate === 0 || sendAmount <= 0) {
    return [];
  }

  const deliveryFilter = options?.deliveryMethod || "all";

  // Filter methods by delivery method
  const filteredMethods = deliveryFilter === "all"
    ? PAYMENT_METHODS
    : PAYMENT_METHODS.filter((m) => m.deliveryMethod === deliveryFilter);

  return filteredMethods.map((method) => {
    // Volume discount for bank methods: reduce % fee for large amounts
    let adjustedFlatFeePercent = method.flatFeePercent;
    if (method.type === "bank" || method.type === "papss") {
      if (sendAmount > 50000) {
        adjustedFlatFeePercent *= 0.7; // 30% discount
      } else if (sendAmount > 5000) {
        adjustedFlatFeePercent *= 0.85; // 15% discount
      }
    }

    // Applied exchange rate (mid-market + markup)
    const adjustedRate = midMarketRate * (1 - method.fxMarkupPercent / 100);

    // Flat fee in send currency (with volume discount applied)
    const flatFee = Math.max(
      method.flatFeeMin,
      Math.min(sendAmount * (adjustedFlatFeePercent / 100), method.flatFeeMax)
    );

    // Amount after fee (in send currency)
    const amountAfterFee = sendAmount - flatFee;

    // Convert to receive currency at adjusted rate
    const recipientGets = Math.max(0, amountAfterFee * adjustedRate);

    // Total cost breakdown
    const totalFee = sendAmount - (recipientGets / midMarketRate);
    const totalFeePercent = (totalFee / sendAmount) * 100;

    return {
      method: method.name,
      methodType: method.type,
      recipientGets: Math.round(recipientGets * 100) / 100,
      totalFee: Math.round(totalFee * 100) / 100,
      totalFeePercent: Math.round(totalFeePercent * 100) / 100,
      exchangeRate: Math.round(adjustedRate * 10000) / 10000,
      exchangeRateMarkup: method.fxMarkupPercent,
      speed: method.speed,
      speedRank: method.speedRank,
      reliability: method.reliability,
      colorClass: method.colorClass,
      deliveryMethod: method.deliveryMethod,
    };
  }).sort((a, b) => b.recipientGets - a.recipientGets); // Best value first
}

/**
 * Calculate savings of using PAPSS vs the next best alternative.
 */
export function calculateSavings(results: PaymentMethodResult[]): {
  bestMethod: PaymentMethodResult;
  secondBest: PaymentMethodResult | null;
  savingsAmount: number;
  savingsPercent: number;
} | null {
  if (results.length < 2) return null;

  const sorted = [...results].sort((a, b) => b.recipientGets - a.recipientGets);
  const best = sorted[0];
  const second = sorted[1];

  if (!second || second.recipientGets === 0) return null;

  const savingsAmount = second.recipientGets - best.recipientGets;
  const savingsPercent = (savingsAmount / second.recipientGets) * 100;

  return {
    bestMethod: best,
    secondBest: second,
    savingsAmount: Math.round(savingsAmount * 100) / 100,
    savingsPercent: Math.round(savingsPercent * 100) / 100,
  };
}
