"use client";

import { useEffect, useState } from "react";

/**
 * Dismissible banner shown when the browser goes offline.
 * Auto-dismisses when connectivity is restored.
 * Per docs/agents/offline-caching.md and docs/agents/error-handling.md.
 */
export default function OfflineBanner() {
  const [isOffline, setIsOffline] = useState(false);
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    // Sync with current state after hydration
    setIsOffline(!navigator.onLine);

    const handleOffline = () => {
      setIsOffline(true);
      setDismissed(false);
    };
    const handleOnline = () => {
      setIsOffline(false);
      setDismissed(false);
    };

    window.addEventListener("offline", handleOffline);
    window.addEventListener("online", handleOnline);

    return () => {
      window.removeEventListener("offline", handleOffline);
      window.removeEventListener("online", handleOnline);
    };
  }, []);

  if (!isOffline || dismissed) return null;

  return (
    <div
      role="alert"
      aria-live="polite"
      data-testid="offline-banner"
      className="fixed bottom-4 left-1/2 z-50 flex -translate-x-1/2 items-center gap-3 rounded-lg border border-black/20 bg-[var(--color-charcoal)] px-4 py-3 text-sm text-white shadow-lg"
    >
      <span>
        You&apos;re offline. Previously viewed pages are still available.
      </span>
      <button
        type="button"
        onClick={() => setDismissed(true)}
        title="Dismiss offline notification"
        aria-label="Dismiss offline notification"
        className="ml-2 rounded p-1 transition hover:bg-white/20"
      >
        ✕
      </button>
    </div>
  );
}
