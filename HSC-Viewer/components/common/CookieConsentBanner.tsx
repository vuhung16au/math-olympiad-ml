"use client";

import { useEffect, useState } from "react";
import { getPref, PREF_KEYS, setPref } from "@/lib/preferences";

/**
 * One-time notice about functional cookies. Dismissal is stored in
 * `hsc_cookie_consent` (see docs/agents/cookies.md).
 */
export default function CookieConsentBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (getPref(PREF_KEYS.cookieConsent) === "1") {
      return;
    }
    setVisible(true);
  }, []);

  const handleAccept = () => {
    setPref(PREF_KEYS.cookieConsent, "1");
    setVisible(false);
  };

  if (!visible) {
    return null;
  }

  return (
    <div
      role="region"
      aria-label="Cookie notice"
      data-testid="cookie-consent-banner"
      className="fixed bottom-4 left-1/2 z-[60] flex w-[min(100%-2rem,36rem)] -translate-x-1/2 flex-col gap-3 rounded-lg border border-black/10 bg-[var(--color-ivory)] px-4 py-3 text-sm text-[var(--color-charcoal)] shadow-lg sm:flex-row sm:items-center sm:justify-between"
    >
      <p className="m-0 leading-snug">
        We use cookies to remember your booklet, the page you were on, and
        your navigation settings.
      </p>
      <button
        type="button"
        onClick={handleAccept}
        className="shrink-0 rounded-md bg-[var(--color-purple)] px-4 py-2 text-sm font-medium text-white transition hover:opacity-90"
        title="Accept and dismiss cookie notice"
        aria-label="Accept and dismiss cookie notice"
      >
        Accept
      </button>
    </div>
  );
}
