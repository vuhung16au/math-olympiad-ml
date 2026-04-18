/**
 * Lightweight cookie-based user preferences.
 * All cookies are SameSite=Lax, path=/ and expire after 1 year.
 */

const ONE_YEAR_SECONDS = 60 * 60 * 24 * 365;

export type ResumeMode = "auto" | "prompt" | "off";

const LAST_PAGE_ENTRY_DELIMITER = ",";
const LAST_PAGE_VALUE_DELIMITER = ":";

function setCookie(name: string, value: string): void {
  if (typeof document === "undefined") return;
  const secureFlag = window.location.protocol === "https:" ? "; Secure" : "";
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; path=/; max-age=${ONE_YEAR_SECONDS}; SameSite=Lax${secureFlag}`;
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
  lastPageBySlug: "hsc_last_page_by_slug",
  lastSlug: "hsc_last_slug",
  resumeMode: "hsc_resume_mode",
  viewMode: "hsc_view_mode",
  readingTheme: "hsc_reading_theme",
  scale: "hsc_scale",
  outlineTab: "hsc_outline_tab",
  navPanelPos: "hsc_nav_panel_pos",
} as const;

export function getPref(key: string): string | null {
  return getCookie(key);
}

export function setPref(key: string, value: string): void {
  setCookie(key, value);
}

function parseLastPageBySlugCookie(raw: string | null): Record<string, number> {
  if (!raw) {
    return {};
  }

  const map: Record<string, number> = {};

  for (const entry of raw.split(LAST_PAGE_ENTRY_DELIMITER)) {
    const trimmed = entry.trim();
    if (!trimmed) {
      continue;
    }

    const [slugPart, pagePart] = trimmed.split(LAST_PAGE_VALUE_DELIMITER);
    if (!slugPart || !pagePart) {
      continue;
    }

    const slug = slugPart.trim();
    const page = Number(pagePart.trim());
    if (!slug || !Number.isSafeInteger(page) || page < 1) {
      continue;
    }

    map[slug] = page;
  }

  return map;
}

function serializeLastPageBySlugCookie(map: Record<string, number>): string {
  return Object.entries(map)
    .filter(([slug, page]) => slug && Number.isSafeInteger(page) && page >= 1)
    .map(([slug, page]) => `${slug}${LAST_PAGE_VALUE_DELIMITER}${page}`)
    .join(LAST_PAGE_ENTRY_DELIMITER);
}

export function getLastPageForSlug(slug: string): number | null {
  if (!slug) {
    return null;
  }

  const map = parseLastPageBySlugCookie(getPref(PREF_KEYS.lastPageBySlug));
  return map[slug] ?? null;
}

export function setLastPageForSlug(slug: string, page: number): void {
  if (!slug || !Number.isSafeInteger(page) || page < 1) {
    return;
  }

  const map = parseLastPageBySlugCookie(getPref(PREF_KEYS.lastPageBySlug));
  map[slug] = page;
  setPref(PREF_KEYS.lastPageBySlug, serializeLastPageBySlugCookie(map));
}

export function getResumeMode(): ResumeMode {
  const mode = getPref(PREF_KEYS.resumeMode);
  if (mode === "off" || mode === "prompt" || mode === "auto") {
    return mode;
  }

  return "auto";
}
