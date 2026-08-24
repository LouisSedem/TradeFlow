"use client";

import { useState, useCallback, useMemo } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import {
  ArrowDownUp,
  ArrowRight,
  CheckCircle2,
  Clock,
  Loader2,
  AlertCircle,
  TrendingDown,
  Zap,
  Shield,
  BarChart3,
  Building2,
  Smartphone,
  Wallet,
  Radio,
} from "lucide-react";
import { RateChart } from "./rate-chart";
import { RateAlertDialog } from "./rate-alert-dialog";

interface CurrencyOption {
  code: string;
  name: string;
  symbol: string;
  flag: string;
  country: string;
  papssLive: boolean;
}

interface MethodResult {
  method: string;
  methodType: string;
  recipientGets: number;
  totalFee: number;
  totalFeePercent: number;
  exchangeRate: number;
  speed: string;
  speedRank: number;
  reliability: string;
  colorClass: string;
}

interface Savings {
  bestMethod: MethodResult;
  secondBest: MethodResult;
  savingsAmount: number;
  savingsPercent: number;
}

interface CompareResponse {
  sendCurrencyInfo: { code: string; symbol: string; flag: string; name: string };
  receiveCurrencyInfo: { code: string; symbol: string; flag: string; name: string };
  midMarketRate: number;
  methods: MethodResult[];
  savings: Savings | null;
  rateSource: string;
  rateFetchedAt: string | null;
}

// Popular send amounts
const QUICK_AMOUNTS = [1000, 5000, 10000, 50000, 100000];

const METHOD_ICONS: Record<string, React.ReactNode> = {
  papss: <Zap className="w-4 h-4" />,
  bank: <Shield className="w-4 h-4" />,
  fintech: <BarChart3 className="w-4 h-4" />,
  mto: <AlertCircle className="w-4 h-4" />,
};

const BADGE_STYLES: Record<string, string> = {
  emerald: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800",
  slate: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border-slate-200 dark:border-slate-700",
  amber: "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300 border-amber-200 dark:border-amber-800",
  yellow: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800",
  orange: "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300 border-orange-200 dark:border-orange-800",
};

type DeliveryFilter = "all" | "bank_deposit" | "mobile_money" | "cash_pickup";

const DELIVERY_OPTIONS: { value: DeliveryFilter; label: string; icon: React.ReactNode }[] = [
  { value: "all", label: "All Methods", icon: <BarChart3 className="w-3.5 h-3.5" /> },
  { value: "bank_deposit", label: "Bank Deposit", icon: <Building2 className="w-3.5 h-3.5" /> },
  { value: "mobile_money", label: "Mobile Money", icon: <Smartphone className="w-3.5 h-3.5" /> },
  { value: "cash_pickup", label: "Cash Pickup", icon: <Wallet className="w-3.5 h-3.5" /> },
];

export function FxCalculator({ currencies }: { currencies: CurrencyOption[] }) {
  const [sendCurrency, setSendCurrency] = useState("GHS");
  const [receiveCurrency, setReceiveCurrency] = useState("KES");
  const [amount, setAmount] = useState("10000");
  const [result, setResult] = useState<CompareResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [deliveryFilter, setDeliveryFilter] = useState<DeliveryFilter>("all");
  const [alertOpen, setAlertOpen] = useState(false);

  const handleSwap = useCallback(() => {
    setSendCurrency(receiveCurrency);
    setReceiveCurrency(sendCurrency);
    setResult(null);
  }, [sendCurrency, receiveCurrency]);

  const handleCompare = useCallback(async () => {
    const numAmount = parseFloat(amount);
    if (isNaN(numAmount) || numAmount <= 0) {
      setError("Enter a valid amount");
      return;
    }
    if (sendCurrency === receiveCurrency) {
      setError("Select different currencies");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/fx/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sendCurrency,
          receiveCurrency,
          sendAmount: numAmount,
          deliveryMethod: deliveryFilter,
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Comparison failed");
      }
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }, [amount, sendCurrency, receiveCurrency, deliveryFilter]);

  const sendCur = useMemo(() => currencies.find((c) => c.code === sendCurrency), [currencies, sendCurrency]);
  const recvCur = useMemo(() => currencies.find((c) => c.code === receiveCurrency), [currencies, receiveCurrency]);

  const isLive = result?.rateSource?.includes("live") ?? false;

  const formatTime = (isoStr: string | null) => {
    if (!isoStr) return "N/A";
    const d = new Date(isoStr);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  return (
    <section className="w-full max-w-2xl mx-auto" aria-label="FX Comparison Calculator">
      <Card className="border-2 border-emerald-200 dark:border-emerald-900/50 shadow-lg shadow-emerald-500/5">
        <CardContent className="p-4 sm:p-6 space-y-5">
          {/* Send side */}
          <div className="space-y-2">
            <label htmlFor="send-amount" className="text-sm font-medium text-muted-foreground">
              You send
            </label>
            <div className="flex gap-3">
              <Input
                id="send-amount"
                type="number"
                inputMode="decimal"
                placeholder="0.00"
                value={amount}
                onChange={(e) => { setAmount(e.target.value); setResult(null); }}
                className="flex-1 text-lg font-semibold h-12"
                min="1"
                step="any"
                aria-label="Amount to send"
              />
              <Select value={sendCurrency} onValueChange={(v) => { setSendCurrency(v); setResult(null); }}>
                <SelectTrigger className="w-[160px] h-12" aria-label="Send currency">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {currencies.map((c) => (
                    <SelectItem key={c.code} value={c.code}>
                      <span className="mr-1.5">{c.flag}</span> {c.code}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            {/* Quick amount buttons */}
            <div className="flex flex-wrap gap-2">
              {QUICK_AMOUNTS.filter((a) => {
                if (sendCurrency === "GHS") return a <= 100000;
                if (sendCurrency === "NGN") return a >= 5000;
                if (sendCurrency === "ZAR") return a <= 100000;
                return true;
              }).map((qa) => (
                <button
                  key={qa}
                  onClick={() => { setAmount(String(qa)); setResult(null); }}
                  className={`px-3 py-1 text-xs font-medium rounded-full border transition-colors cursor-pointer ${
                    amount === String(qa)
                      ? "bg-emerald-100 text-emerald-700 border-emerald-300 dark:bg-emerald-900/40 dark:text-emerald-300 dark:border-emerald-700"
                      : "bg-muted/50 text-muted-foreground border-border hover:bg-muted"
                  }`}
                >
                  {sendCur?.symbol}{qa.toLocaleString()}
                </button>
              ))}
            </div>
          </div>

          {/* Swap button */}
          <div className="flex justify-center -my-1">
            <Button
              variant="outline"
              size="icon"
              onClick={handleSwap}
              className="rounded-full h-10 w-10 border-2 border-dashed"
              aria-label="Swap currencies"
            >
              <ArrowDownUp className="h-4 w-4" />
            </Button>
          </div>

          {/* Receive side */}
          <div className="space-y-2">
            <label htmlFor="recv-currency" className="text-sm font-medium text-muted-foreground">
              They receive
            </label>
            <Select value={receiveCurrency} onValueChange={(v) => { setReceiveCurrency(v); setResult(null); }}>
              <SelectTrigger id="recv-currency" className="w-full h-12" aria-label="Receive currency">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {currencies
                  .filter((c) => c.code !== sendCurrency)
                  .map((c) => (
                    <SelectItem key={c.code} value={c.code}>
                      <span className="mr-1.5">{c.flag}</span> {c.code} — {c.name}
                      {c.papssLive && (
                        <span className="ml-1.5 text-[10px] font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/30 px-1.5 py-0.5 rounded-full">
                          PAPSS
                        </span>
                      )}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </div>

          {/* Delivery method filter pills */}
          <div className="space-y-1.5">
            <label className="text-xs font-medium text-muted-foreground">Delivery method</label>
            <div className="flex flex-wrap gap-2">
              {DELIVERY_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => { setDeliveryFilter(opt.value); setResult(null); }}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full border transition-colors cursor-pointer ${
                    deliveryFilter === opt.value
                      ? "bg-emerald-100 text-emerald-700 border-emerald-300 dark:bg-emerald-900/40 dark:text-emerald-300 dark:border-emerald-700"
                      : "bg-muted/50 text-muted-foreground border-border hover:bg-muted"
                  }`}
                >
                  {opt.icon}
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* Compare button */}
          <Button
            onClick={handleCompare}
            disabled={loading || !amount || parseFloat(amount) <= 0}
            className="w-full h-12 text-base font-semibold bg-emerald-600 hover:bg-emerald-700 text-white cursor-pointer"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Comparing...
              </>
            ) : (
              <>
                Compare Payment Methods
                <ArrowRight className="ml-2 h-4 w-4" />
              </>
            )}
          </Button>

          {error && (
            <p className="text-sm text-destructive flex items-center gap-1.5" role="alert">
              <AlertCircle className="h-4 w-4 shrink-0" />
              {error}
            </p>
          )}
        </CardContent>
      </Card>

      {/* Results */}
      {result && (
        <div className="mt-6 space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
          {/* Savings banner */}
          {result.savings && result.savings.bestMethod.methodType === "papss" && (
            <Card className="border-emerald-300 dark:border-emerald-700 bg-emerald-50 dark:bg-emerald-950/30">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center">
                  <TrendingDown className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-emerald-800 dark:text-emerald-200">
                    Save {recvCur?.symbol}{result.savings.savingsAmount.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                  </p>
                  <p className="text-sm text-emerald-600 dark:text-emerald-400">
                    {result.savings.savingsPercent}% more received with PAPSS vs {result.savings.secondBest.method}
                  </p>
                </div>
                <CheckCircle2 className="h-6 w-6 text-emerald-500 flex-shrink-0" />
              </CardContent>
            </Card>
          )}

          {/* Method comparison cards */}
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-muted-foreground px-1">
              Comparison ({sendCur?.symbol}{parseFloat(amount).toLocaleString()})
              {deliveryFilter !== "all" && (
                <span className="ml-2 text-emerald-600 dark:text-emerald-400">
                  · {DELIVERY_OPTIONS.find(o => o.value === deliveryFilter)?.label}
                </span>
              )}
            </h3>
            {result.methods.map((method, i) => {
              const isBest = i === 0;
              const isPapss = method.methodType === "papss";
              return (
                <Card
                  key={method.method}
                  className={`${
                    isBest
                      ? "border-2 border-emerald-300 dark:border-emerald-700 shadow-md"
                      : "border border-border"
                  } transition-all`}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-3 min-w-0">
                        <div className={`flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center text-white ${
                          isPapss ? "bg-emerald-500" : "bg-muted-foreground/30"
                        }`}>
                          {METHOD_ICONS[method.methodType] || <BarChart3 className="w-4 h-4" />}
                        </div>
                        <div className="min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="font-semibold text-sm">{method.method}</span>
                            <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${BADGE_STYLES[method.colorClass] || ""}`}>
                              {method.totalFeePercent}% fee
                            </span>
                            {isBest && (
                              <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">
                                BEST VALUE
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {method.speed}
                            </span>
                            <span>Rate: {method.exchangeRate}</span>
                          </div>
                        </div>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <p className={`text-lg font-bold ${isPapss ? "text-emerald-600 dark:text-emerald-400" : ""}`}>
                          {result.receiveCurrencyInfo.symbol}
                          {method.recipientGets.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Fee: {result.sendCurrencyInfo.symbol}{method.totalFee.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Mid-market rate note with source info */}
          <div className="text-center px-2 space-y-1">
            <p className="text-xs text-muted-foreground">
              Mid-market rate: 1 {result.sendCurrencyInfo.code} = {result.midMarketRate.toFixed(4)} {result.receiveCurrencyInfo.code}.
              Actual rates may vary. Comparison based on publicly available fee structures.
            </p>
            <p className="text-xs text-muted-foreground flex items-center justify-center gap-1.5">
              {isLive ? (
                <span className="inline-flex items-center gap-1">
                  <Radio className="h-3 w-3 text-emerald-500" />
                  <span className="font-medium text-emerald-600 dark:text-emerald-400">Live</span>
                </span>
              ) : (
                <span className="font-medium">Estimated</span>
              )}
              <span>·</span>
              <span>Source: {result.rateSource}</span>
              {result.rateFetchedAt && (
                <>
                  <span>·</span>
                  <span>Updated: {formatTime(result.rateFetchedAt)}</span>
                </>
              )}
            </p>
          </div>

          {/* Rate chart */}
          <RateChart
            sendCurrency={sendCurrency}
            receiveCurrency={receiveCurrency}
            currentRate={result.midMarketRate}
          />

          {/* Set Rate Alert button */}
          <div className="flex justify-center">
            <Button
              variant="outline"
              onClick={() => setAlertOpen(true)}
              className="text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/30 cursor-pointer"
            >
              <BarChart3 className="mr-2 h-4 w-4" />
              Set Rate Alert
            </Button>
          </div>

          <RateAlertDialog
            open={alertOpen}
            onOpenChange={setAlertOpen}
            sendCurrency={sendCurrency}
            receiveCurrency={receiveCurrency}
            currentRate={result.midMarketRate}
            sendSymbol={sendCur?.symbol || ""}
            receiveSymbol={recvCur?.symbol || ""}
          />
        </div>
      )}
    </section>
  );
}