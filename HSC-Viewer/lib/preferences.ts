/**
 * Lightweight cookie-based user preferences.
 * All cookies are SameSite=Lax, path=/ and expire after 1 year.
 */

const ONE_YEAR_SECONDS = 60 * 60 * 24 * 365;

function setCookie(name: string, value: string): void {
  if (typeof document === "undefined") return;
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; path=/; max-age=${ONE_YEAR_SECONDS}; SameSite=Lax`;
}

function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const key = `${encodeURIComponent(name)}=`;
  for (const part of document.cookie.split(";")) {
    const trimmed = part.trim();
    if (trimmed.startsWith(key)) {
      return decodeURIComponent(trimmed.slice(key.length));
    }
  }
  return null;
}

export const PREF_KEYS = {
  sidebarCollapsed: "hsc_sidebar_collapsed",
  lastUrl: "hsc_last_url",
  viewMode: "hsc_view_mode",
  readingTheme: "hsc_reading_theme",
  scale: "hsc_scale",
} as const;

export function getPref(key: string): string | null {
  return getCookie(key);
}

export function setPref(key: string, value: string): void {
  setCookie(key, value);
}
