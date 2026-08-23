import type { Metadata, Viewport } from "next";
import { Geist } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "next-themes";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TradeFlow — Compare African Cross-Border Payment Costs",
  description:
    "See how much you save with PAPSS vs traditional methods. Instant comparison for 20+ African currencies. Built for AfCFTA traders.",
  keywords: [
    "PAPSS",
    "AfCFTA",
    "cross-border payments",
    "African trade",
    "FX comparison",
    "Afreximbank",
    "send money Africa",
    "business payments Africa",
  ],
};

export const viewport: Viewport = {
  themeColor: "#059669",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${geistSans.variable} font-sans antialiased bg-background text-foreground`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
