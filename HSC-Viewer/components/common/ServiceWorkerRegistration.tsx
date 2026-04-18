"use client";

import { useEffect } from "react";

/**
 * Registers /sw.js after hydration.
 * Per docs/agents/offline-caching.md — must be mounted in the root layout.
 */
export default function ServiceWorkerRegistration() {
  useEffect(() => {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js").catch((err) => {
        console.warn("[SW] Registration failed:", err);
      });
    }
  }, []);

  return null;
}
