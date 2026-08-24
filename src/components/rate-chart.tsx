"use client";

import { useMemo, useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import { Card, CardContent } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Minus, BarChart3, Loader2 } from "lucide-react";
import { generateRateHistory, getRateStats, type RateHistoryPoint } from "@/lib/rate-history";

interface RateChartProps {
  sendCurrency: string;
  receiveCurrency: string;
  currentRate: number;
}

interface ApiHistoryResponse {
  data: RateHistoryPoint[];
  source: string;
}

export function RateChart({ sendCurrency, receiveCurrency, currentRate }: RateChartProps) {
  const [apiData, setApiData] = useState<RateHistoryPoint[] | null>(null);
  const [source, setSource] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(`/api/fx/history?send=${sendCurrency}&receive=${receiveCurrency}&days=30`)
      .then((res) => res.json())
      .then((json: ApiHistoryResponse) => {
        if (!cancelled) {
          setApiData(json.data);
          setSource(json.source);
          setLoading(false);
        }
      })
      .catch(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [sendCurrency, receiveCurrency]);

  const history = useMemo(() => {
    if (apiData && apiData.length >= 7) return apiData;
    return generateRateHistory(currentRate);
  }, [apiData, currentRate]);

  const stats = useMemo(() => getRateStats(history), [history]);
  const isRealData = source.includes("live");

  const formatDate = (dateStr: string) => {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  };

  const decimals = currentRate > 100 ? 0 : currentRate > 10 ? 2 : 4;

  const TrendIcon = stats.trend === "up" ? TrendingUp : stats.trend === "down" ? TrendingDown : Minus;
  const trendColor = stats.trend === "up" ? "text-emerald-600 dark:text-emerald-400" : stats.trend === "down" ? "text-red-500 dark:text-red-400" : "text-muted-foreground";

  return (
    <Card className="border border-border">
      <CardContent className="p-4 sm:p-6 space-y-4">
        <div className="flex items-center gap-2">
          <BarChart3 className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
          <h3 className="text-sm font-semibold">30-Day Rate Trend</h3>
          <span className="text-xs text-muted-foreground">
            1 {sendCurrency} = ? {receiveCurrency}
          </span>
          {isRealData && (
            <span className="text-[10px] font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-0.5 rounded-full">
              Live Data
            </span>
          )}
        </div>

        {loading ? (
          <div className="h-48 sm:h-56 w-full flex items-center justify-center">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <div className="h-48 sm:h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={history} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                <defs>
                  <linearGradient id="rateGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#059669" stopOpacity={0.2} />
                    <stop offset="100%" stopColor="#059669" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis
                  dataKey="date"
                  tickFormatter={formatDate}
                  tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                  axisLine={false}
                  tickLine={false}
                  interval={4}
                />
                <YAxis
                  domain={["auto", "auto"]}
                  tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v) => v.toFixed(decimals)}
                  width={60}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--popover))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                    fontSize: "12px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                  }}
                  labelFormatter={formatDate}
                  formatter={(value: number) => [value.toFixed(decimals), `${sendCurrency}/${receiveCurrency}`]}
                />
                <Area
                  type="monotone"
                  dataKey="rate"
                  stroke="#059669"
                  strokeWidth={2}
                  fill="url(#rateGradient)"
                  dot={false}
                  activeDot={{ r: 4, fill: "#059669", strokeWidth: 0 }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-3 text-center">
          <div>
            <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Min</p>
            <p className="text-sm font-semibold">{stats.min.toFixed(decimals)}</p>
          </div>
          <div className="flex flex-col items-center">
            <p className="text-[10px] uppercase tracking-wide text-muted-foreground">30d Trend</p>
            <div className={`flex items-center gap-1 ${trendColor}`}>
              <TrendIcon className="h-3.5 w-3.5" />
              <span className="text-sm font-semibold">{stats.trend === "up" ? "Up" : stats.trend === "down" ? "Down" : "Flat"}</span>
            </div>
          </div>
          <div>
            <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Max</p>
            <p className="text-sm font-semibold">{stats.max.toFixed(decimals)}</p>
          </div>
        </div>
        <p className="text-[10px] text-center text-muted-foreground">
          Range: {stats.range.toFixed(decimals)}
          {isRealData ? "" : " · Simulated for illustration"}
        </p>
      </CardContent>
    </Card>
  );
}