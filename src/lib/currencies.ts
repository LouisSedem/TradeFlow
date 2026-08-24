/**
 * African currencies supported by PAPSS / AfCFTA trade corridors.
 * Rates are approximations of mid-market rates vs USD.
 * In production, these would be fetched live from central bank APIs.
 */

export interface Currency {
  code: string;        // ISO 4217
  name: string;        // Full name
  symbol: string;       // Display symbol
  flag: string;        // Country flag emoji
  country: string;      // Country name
  countryAlpha2: string; // ISO 3166-1 alpha-2
  rateToUSD: number;   // 1 unit of this currency = ? USD
  papssLive: boolean;  // Whether PAPSS supports this currency
  afcftaMember: boolean;
}

// Approximate rates as of 2025. Updated via central bank sources.
// In production: fetch from Bank of Ghana, CBK, CBN, etc.
export const AFRICAN_CURRENCIES: Currency[] = [
  // West Africa
  { code: "GHS", name: "Ghanaian Cedi", symbol: "GH\u20B5", flag: "\u{1F1EC}\u{1F1ED}", country: "Ghana", countryAlpha2: "GH", rateToUSD: 0.0647, papssLive: true, afcftaMember: true },
  { code: "NGN", name: "Nigerian Naira", symbol: "\u20A6", flag: "\u{1F1F3}\u{1F1EC}", country: "Nigeria", countryAlpha2: "NG", rateToUSD: 0.000635, papssLive: true, afcftaMember: true },
  { code: "XOF", name: "West African CFA Franc", symbol: "CFA", flag: "\u{1F1EB}\u{1F1F7}", country: "Senegal", countryAlpha2: "SN", rateToUSD: 0.00164, papssLive: true, afcftaMember: true },
  { code: "XOF", name: "West African CFA Franc", symbol: "CFA", flag: "\u{1F1EE}\u{1F1F9}", country: "C\u00F4te d'Ivoire", countryAlpha2: "CI", rateToUSD: 0.00164, papssLive: true, afcftaMember: true },

  // East Africa
  { code: "KES", name: "Kenyan Shilling", symbol: "KSh", flag: "\u{1F1F0}\u{1F1EA}", country: "Kenya", countryAlpha2: "KE", rateToUSD: 0.00772, papssLive: true, afcftaMember: true },
  { code: "TZS", name: "Tanzanian Shilling", symbol: "TSh", flag: "\u{1F1F9}\u{1F1FF}", country: "Tanzania", countryAlpha2: "TZ", rateToUSD: 0.000383, papssLive: true, afcftaMember: true },
  { code: "UGX", name: "Ugandan Shilling", symbol: "USh", flag: "\u{1F1FA}\u{1F1EC}", country: "Uganda", countryAlpha2: "UG", rateToUSD: 0.000271, papssLive: true, afcftaMember: true },
  { code: "RWF", name: "Rwandan Franc", symbol: "FRw", flag: "\u{1F1F7}\u{1F1FC}", country: "Rwanda", countryAlpha2: "RW", rateToUSD: 0.000773, papssLive: true, afcftaMember: true },
  { code: "ETB", name: "Ethiopian Birr", symbol: "Br", flag: "\u{1F1EA}\u{1F1F9}", country: "Ethiopia", countryAlpha2: "ET", rateToUSD: 0.00813, papssLive: false, afcftaMember: true },

  // Southern Africa
  { code: "ZAR", name: "South African Rand", symbol: "R", flag: "\u{1F1FF}\u{1F1E6}", country: "South Africa", countryAlpha2: "ZA", rateToUSD: 0.0544, papssLive: true, afcftaMember: true },
  { code: "BWP", name: "Botswana Pula", symbol: "P", flag: "\u{1F1E7}\u{1F1FC}", country: "Botswana", countryAlpha2: "BW", rateToUSD: 0.0741, papssLive: true, afcftaMember: true },
  { code: "NAD", name: "Namibian Dollar", symbol: "N$", flag: "\u{1F1F3}\u{1F1E6}", country: "Namibia", countryAlpha2: "NA", rateToUSD: 0.0544, papssLive: false, afcftaMember: true },
  { code: "MWK", name: "Malawian Kwacha", symbol: "MK", flag: "\u{1F1F2}\u{1F1FC}", country: "Malawi", countryAlpha2: "MW", rateToUSD: 0.000576, papssLive: false, afcftaMember: true },
  { code: "ZMW", name: "Zambian Kwacha", symbol: "ZK", flag: "\u{1F1FF}\u{1F1F2}", country: "Zambia", countryAlpha2: "ZM", rateToUSD: 0.0362, papssLive: true, afcftaMember: true },

  // North Africa
  { code: "EGP", name: "Egyptian Pound", symbol: "E\u00A3", flag: "\u{1F1EA}\u{1F1EC}", country: "Egypt", countryAlpha2: "EG", rateToUSD: 0.0202, papssLive: true, afcftaMember: true },
  { code: "MAD", name: "Moroccan Dirham", symbol: "MAD", flag: "\u{1F1F2}\u{1F1E6}", country: "Morocco", countryAlpha2: "MA", rateToUSD: 0.100, papssLive: false, afcftaMember: true },
  { code: "TND", name: "Tunisian Dinar", symbol: "DT", flag: "\u{1F1F9}\u{1F1F3}", country: "Tunisia", countryAlpha2: "TN", rateToUSD: 0.316, papssLive: false, afcftaMember: true },

  // Central Africa
  { code: "XAF", name: "Central African CFA Franc", symbol: "FCFA", flag: "\u{1F1E8}\u{1F1F2}", country: "Cameroon", countryAlpha2: "CM", rateToUSD: 0.00164, papssLive: true, afcftaMember: true },
  { code: "CDF", name: "Congolese Franc", symbol: "FC", flag: "\u{1F1E8}\u{1F1E9}", country: "DR Congo", countryAlpha2: "CD", rateToUSD: 0.000352, papssLive: false, afcftaMember: true },

  // Major (for comparison baseline)
  { code: "USD", name: "US Dollar", symbol: "$", flag: "\u{1F1FA}\u{1F1F8}", country: "United States", countryAlpha2: "US", rateToUSD: 1.0, papssLive: false, afcftaMember: false },
  { code: "EUR", name: "Euro", symbol: "\u20AC", flag: "\u{1F1EA}\u{1F1FA}", country: "European Union", countryAlpha2: "EU", rateToUSD: 1.085, papssLive: false, afcftaMember: false },
  { code: "GBP", name: "British Pound", symbol: "\u00A3", flag: "\u{1F1EC}\u{1F1E7}", country: "United Kingdom", countryAlpha2: "GB", rateToUSD: 1.27, papssLive: false, afcftaMember: false },
];

/** Get unique currency codes with their best representation */
export function getUniqueCurrencies(): Currency[] {
  const seen = new Set<string>();
  return AFRICAN_CURRENCIES.filter((c) => {
    if (seen.has(c.code)) return false;
    seen.add(c.code);
    return true;
  });
}

/** Get currencies that are PAPSS-enabled */
export function getPapssCurrencies(): Currency[] {
  return getUniqueCurrencies().filter((c) => c.papssLive);
}

/** Get currency by code */
export function getCurrency(code: string): Currency | undefined {
  return AFRICAN_CURRENCIES.find((c) => c.code === code);
}

/** Cross rate: how many quoteCurrency units per 1 baseCurrency unit */
export function getCrossRate(baseCode: string, quoteCode: string, liveRates?: Map<string, number>): number {
  if (baseCode === quoteCode) return 1;

  // Use live rates if provided
  if (liveRates) {
    const baseToUsd = liveRates.get(baseCode);
    const quoteToUsd = liveRates.get(quoteCode);
    if (baseToUsd && quoteToUsd && quoteToUsd > 0) {
      return baseToUsd / quoteToUsd;
    }
  }

  // Fallback to hardcoded rates
  const base = AFRICAN_CURRENCIES.find((c) => c.code === baseCode);
  const quote = AFRICAN_CURRENCIES.find((c) => c.code === quoteCode);
  if (!base || !quote) return 0;
  // base → USD → quote
  return base.rateToUSD / quote.rateToUSD;
}

