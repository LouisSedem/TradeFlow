"use client";

// Minimal toast hook compatible with shadcn toaster component
import { toast as sonnerToast } from "sonner";

export function useToast() {
  return {
    toast: sonnerToast,
    dismiss: (id?: string) => {
      // sonner handles dismiss internally
    },
  };
}

export { toast } from "sonner";
