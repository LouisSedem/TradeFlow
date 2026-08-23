import { Suspense } from "react";
import { FxCalculator } from "@/components/fx-calculator";
import { getUniqueCurrencies } from "@/lib/currencies";
import {
  ArrowRight,
  Zap,
  Shield,
  Clock,
  Globe2,
  TrendingDown,
  Building2,
  Users,
} from "lucide-react";

function CalculatorLoader() {
  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="h-80 animate-pulse bg-muted rounded-xl"></div>
    </div>
  );
}

export default function Page() {
  const currencies = getUniqueCurrencies();
  const papssCurrencies = currencies.filter((c) => c.papssLive).length;
  const africanCurrencies = currencies.filter((c) => c.afcftaMember).length;

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center">
              <Zap className="h-4 w-4 text-white" />
            </div>
            <span className="font-bold text-lg tracking-tight">TradeFlow</span>
          </div>
          <nav className="hidden sm:flex items-center gap-6 text-sm text-muted-foreground">
            <a href="#calculator" className="hover:text-foreground transition-colors">Calculator</a>
            <a href="#how-it-works" className="hover:text-foreground transition-colors">How PAPSS Works</a>
            <a href="#features" className="hover:text-foreground transition-colors">Features</a>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero */}
        <section className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-emerald-50/50 to-transparent dark:from-emerald-950/20 dark:to-transparent pointer-events-none">
          </div>
          <div className="relative max-w-6xl mx-auto px-4 sm:px-6 pt-12 pb-8 sm:pt-20 sm:pb-12">
            {/* Badge */}
            <div className="flex justify-center mb-6">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 text-xs font-medium rounded-full border bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                Built for AfCFTA and PAPSS
              </span>
            </div>

            {/* Heading */}
            <div className="text-center max-w-2xl mx-auto">
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight leading-tight">
                Stop Overpaying for{" "}
                <span className="text-emerald-600 dark:text-emerald-400">African Cross-Border</span>{" "}
                Payments
              </h1>
              <p className="mt-4 text-base sm:text-lg text-muted-foreground max-w-xl mx-auto">
                Compare PAPSS against banks, MTOs, and mobile money. See exactly what your recipient receives before you send.
              </p>
            </div>

            {/* Stats */}
            <div className="flex flex-wrap justify-center gap-6 sm:gap-10 mt-8 mb-10 text-center">
              <div>
                <p className="text-2xl sm:text-3xl font-bold text-emerald-600 dark:text-emerald-400">{papssCurrencies}+</p>
                <p className="text-xs sm:text-sm text-muted-foreground">PAPSS Currencies</p>
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-bold">{africanCurrencies}</p>
                <p className="text-xs sm:text-sm text-muted-foreground">African Currencies</p>
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-bold">80%</p>
                <p className="text-xs sm:text-sm text-muted-foreground">Avg. Cost Savings</p>
              </div>
              <div>
                <p className="text-2xl sm:text-3xl font-bold">Instant</p>
                <p className="text-xs sm:text-sm text-muted-foreground">Settlement</p>
              </div>
            </div>
          </div>
        </section>

        {/* Calculator Section */}
        <section id="calculator" className="scroll-mt-16 pb-16 sm:pb-20">
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <Suspense fallback={<CalculatorLoader />}>
              <FxCalculatorWrapper currencies={currencies} />
            </Suspense>
          </div>
        </section>

        {/* How PAPSS Works */}
        <section id="how-it-works" className="scroll-mt-16 py-16 sm:py-20 bg-muted/30">
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <div className="text-center max-w-xl mx-auto mb-12">
              <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
                How PAPSS Works
              </h2>
              <p className="mt-3 text-muted-foreground">
                The Pan-African Payment and Settlement System enables instant payments in local African currencies, no USD conversion needed.
              </p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                {
                  step: "1",
                  title: "You Initiate",
                  desc: "Business in Ghana initiates a payment in Cedis to a supplier in Kenya through their bank.",
                  icon: <Building2 className="w-5 h-5" />,
                },
                {
                  step: "2",
                  title: "PAPSS Routes",
                  desc: "Your bank sends the instruction through PAPSS, which finds the best FX rate.",
                  icon: <Globe2 className="w-5 h-5" />,
                },
                {
                  step: "3",
                  title: "Instant Settlement",
                  desc: "Afreximbank settles the transaction in real-time. No correspondent banks needed.",
                  icon: <Zap className="w-5 h-5" />,
                },
                {
                  step: "4",
                  title: "Supplier Paid",
                  desc: "Supplier in Kenya receives Shillings instantly. No delays, no hidden fees.",
                  icon: <Users className="w-5 h-5" />,
                },
              ].map((item) => (
                <div
                  key={item.step}
                  className="relative bg-background rounded-xl border p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/40 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
                      {item.icon}
                    </div>
                    <div className="w-7 h-7 rounded-full bg-emerald-600 text-white text-sm font-bold flex items-center justify-center">
                      {item.step}
                    </div>
                  </div>
                  <h3 className="font-semibold mb-2">{item.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="scroll-mt-16 py-16 sm:py-20">
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <div className="text-center max-w-xl mx-auto mb-12">
              <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
                Why TradeFlow
              </h2>
              <p className="mt-3 text-muted-foreground">
                Built for African businesses who trade across borders.
              </p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                {
                  title: "Transparent Comparison",
                  desc: "See every fee, every markup, every hidden cost across all payment methods. No surprises.",
                  icon: <TrendingDown className="w-5 h-5" />,
                },
                {
                  title: "PAPSS-First",
                  desc: "Optimised for PAPSS corridors. We show you where PAPSS saves you the most money.",
                  icon: <Zap className="w-5 h-5" />,
                },
                {
                  title: "Instant Settlement",
                  desc: "PAPSS settles in real-time. Your suppliers get paid immediately, not in 3-5 business days.",
                  icon: <Clock className="w-5 h-5" />,
                },
                {
                  title: "20+ African Currencies",
                  desc: "GHS, NGN, KES, ZAR, TZS, UGX and more. Covering all major AfCFTA trade corridors.",
                  icon: <Globe2 className="w-5 h-5" />,
                },
                {
                  title: "No Sign-Up Required",
                  desc: "Use the comparison tool instantly. Create an account when you need invoices and payment tracking.",
                  icon: <Shield className="w-5 h-5" />,
                },
                {
                  title: "SaaS Platform",
                  desc: "Invoicing, payment tracking, and trade tools coming soon. One platform for all your cross-border needs.",
                  icon: <Building2 className="w-5 h-5" />,
                },
              ].map((f) => (
                <div
                  key={f.title}
                  className="rounded-xl border p-6 hover:shadow-md transition-shadow"
                >
                  <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center text-foreground mb-4">
                    {f.icon}
                  </div>
                  <h3 className="font-semibold mb-2">{f.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 sm:py-20 bg-emerald-600 dark:bg-emerald-700">
          <div className="max-w-2xl mx-auto px-4 sm:px-6 text-center">
            <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              Ready to Save on Every Payment?
            </h2>
            <p className="mt-3 text-emerald-100">
              Join the waitlist for early access to invoicing, payment tracking, and trade tools.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row gap-3 justify-center">
              <div className="flex flex-1 sm:max-w-sm">
                <input
                  type="email"
                  placeholder="your@email.com"
                  className="w-full h-12 px-4 rounded-lg border-0 bg-white/10 text-white placeholder:text-white/50 focus:outline-none focus:ring-2 focus:ring-white/30"
                  aria-label="Email for waitlist"
                />
              </div>
              <button className="h-12 px-8 rounded-lg bg-white text-emerald-700 font-semibold hover:bg-emerald-50 transition-colors cursor-pointer">
                Join Waitlist
                <ArrowRight className="inline-block ml-2 h-4 w-4" />
              </button>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t py-8 bg-background">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-emerald-600 flex items-center justify-center">
                <Zap className="h-3 w-3 text-white" />
              </div>
              <span className="font-medium">TradeFlow</span>
            </div>
            <p>Built for the AfCFTA era. Not affiliated with Afreximbank or PAPSS.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FxCalculatorWrapper({ currencies }: { currencies: ReturnType<typeof getUniqueCurrencies> }) {
  const opts = currencies.map((c) => ({
    code: c.code,
    name: c.name,
    symbol: c.symbol,
    flag: c.flag,
    country: c.country,
    papssLive: c.papssLive,
  }));
  return <FxCalculator currencies={opts} />;
}
