"use client";

import { useState } from "react";
import { useSession, signIn, signOut } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { LogIn, LogOut, Loader2, Mail } from "lucide-react";

export function SignInButton() {
  const { data: session, status } = useSession();
  const [open, setOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignIn = async () => {
    if (!email) return;
    setLoading(true);
    try {
      await signIn("dev-credentials", { email, redirect: false });
      setOpen(false);
    } catch {
      // handled by next-auth
    } finally {
      setLoading(false);
    }
  };

  if (status === "loading") {
    return (
      <div className="w-24 h-9 bg-muted animate-pulse rounded-md" />
    );
  }

  if (session?.user?.email) {
    return (
      <div className="flex items-center gap-2">
        <span className="hidden sm:inline text-sm text-muted-foreground truncate max-w-[180px]">
          {session.user.email}
        </span>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => signOut()}
          className="text-muted-foreground hover:text-foreground cursor-pointer"
        >
          <LogOut className="h-4 w-4 mr-1.5" />
          Sign Out
        </Button>
      </div>
    );
  }

  return (
    <>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setOpen(true)}
        className="text-muted-foreground hover:text-foreground cursor-pointer"
      >
        <LogIn className="h-4 w-4 mr-1.5" />
        Sign In
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <LogIn className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
              Sign In to TradeFlow
            </DialogTitle>
            <DialogDescription>
              Enter your email to sign in. No password required.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-2">
            <div className="space-y-1.5">
              <label htmlFor="signin-email" className="text-sm font-medium">
                Email
              </label>
              <Input
                id="signin-email"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSignIn()}
              />
            </div>
          </div>

          <DialogFooter className="sm:justify-end gap-2">
            <Button variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleSignIn}
              disabled={loading || !email}
              className="bg-emerald-600 hover:bg-emerald-700 text-white cursor-pointer"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  <Mail className="h-4 w-4 mr-2" />
                  Sign In
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
