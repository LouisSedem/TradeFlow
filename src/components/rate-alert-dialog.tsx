"use client";

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Bell, Loader2, CheckCircle2, AlertCircle } from "lucide-react";

interface RateAlertDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  sendCurrency: string;
  receiveCurrency: string;
  currentRate: number;
  sendSymbol: string;
  receiveSymbol: string;
}

export function RateAlertDialog({
  open,
  onOpenChange,
  sendCurrency,
  receiveCurrency,
  currentRate,
  sendSymbol,
  receiveSymbol,
}: RateAlertDialogProps) {
  const [email, setEmail] = useState("");
  const [direction, setDirection] = useState<"above" | "below">("above");
  const [targetRate, setTargetRate] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!email || !targetRate) return;

    const numRate = parseFloat(targetRate);
    if (isNaN(numRate) || numRate <= 0) {
      setError("Enter a valid target rate");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/fx/alerts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          baseCurrency: sendCurrency,
          quoteCurrency: receiveCurrency,
          targetRate: numRate,
          direction,
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Failed to create alert");
      }
      setSuccess(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    onOpenChange(false);
    setTimeout(() => {
      setSuccess(false);
      setError(null);
      setEmail("");
      setTargetRate("");
    }, 300);
  };

  const decimals = currentRate > 100 ? 2 : currentRate > 10 ? 4 : 6;

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-md">
        {success ? (
          <>
            <DialogHeader>
              <div className="flex items-center justify-center mb-2">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <CheckCircle2 className="h-6 w-6 text-primary" />
                </div>
              </div>
              <DialogTitle className="text-center">Alert Created!</DialogTitle>
              <DialogDescription className="text-center">
                We&apos;ll email you when 1 {sendCurrency} = {targetRate} {receiveCurrency}
                ({direction === "above" ? "goes above" : "drops below"} your target).
              </DialogDescription>
            </DialogHeader>
            <DialogFooter className="sm:justify-center">
              <Button onClick={handleClose} className="cursor-pointer">
                Done
              </Button>
            </DialogFooter>
          </>
        ) : (
          <>
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-primary" />
                Set Rate Alert
              </DialogTitle>
              <DialogDescription>
                Get notified when the {sendCurrency}/{receiveCurrency} rate hits your target.
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4 py-2">
              {/* Current rate reference */}
              <div className="bg-muted/50 rounded-lg p-3 text-center">
                <p className="text-xs text-muted-foreground">Current rate</p>
                <p className="text-lg font-semibold">
                  1 {sendCurrency} = <span className="text-primary">{currentRate.toFixed(decimals)}</span> {receiveCurrency}
                </p>
              </div>

              {/* Email */}
              <div className="space-y-1.5">
                <Label htmlFor="alert-email">Email</Label>
                <Input
                  id="alert-email"
                  type="email"
                  placeholder="your@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              {/* Direction */}
              <div className="space-y-1.5">
                <Label>Notify me when rate</Label>
                <Select value={direction} onValueChange={(v) => setDirection(v as "above" | "below")}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="above">Goes above target</SelectItem>
                    <SelectItem value="below">Drops below target</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Target rate */}
              <div className="space-y-1.5">
                <Label htmlFor="alert-rate">Target rate (1 {sendCurrency} = ? {receiveCurrency})</Label>
                <Input
                  id="alert-rate"
                  type="number"
                  step="any"
                  placeholder={currentRate.toFixed(decimals)}
                  value={targetRate}
                  onChange={(e) => setTargetRate(e.target.value)}
                />
              </div>

              {error && (
                <p className="text-sm text-destructive flex items-center gap-1.5">
                  <AlertCircle className="h-3.5 w-3.5" />
                  {error}
                </p>
              )}
            </div>

            <DialogFooter className="sm:justify-between gap-2">
              <Button variant="outline" onClick={handleClose}>
                Cancel
              </Button>
              <Button
                onClick={handleSubmit}
                disabled={loading || !email || !targetRate}
                className="cursor-pointer"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating...
                  </>
                ) : (
                  <>
                    <Bell className="mr-2 h-4 w-4" />
                    Create Alert
                  </>
                )}
              </Button>
            </DialogFooter>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}
