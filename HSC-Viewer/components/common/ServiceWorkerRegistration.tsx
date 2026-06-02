"use client";

import { useEffect } from "react";

/**
 * Registers /sw.js after hydration.
 * Per docs/agents/offline-caching.md — must be mounted in the root layout.
 */
export default function ServiceWorkerRegistration() {
  useEffect(() => {
    // Service workers can aggressively cache Next.js documents and cause confusing behavior in `next dev`.
    if (process.env.NODE_ENV !== "production") {
      return;
    }
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js").catch((err) => {
        console.warn("[SW] Registration failed:", err);
      });
    }
  }, []);

  return null;
}
