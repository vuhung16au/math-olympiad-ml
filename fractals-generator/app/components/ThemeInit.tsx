'use client';

import { useEffect } from 'react';

const STORAGE_KEY = 'fg-theme';

export type ThemeMode = 'dark' | 'light';

export function getStoredTheme(): ThemeMode | null {
  if (typeof window === 'undefined') return null;
  const raw = window.localStorage.getItem(STORAGE_KEY);
  return raw === 'light' || raw === 'dark' ? raw : null;
}

export function setTheme(next: ThemeMode): void {
  document.documentElement.dataset.theme = next;
  window.localStorage.setItem(STORAGE_KEY, next);
}

export function ThemeInit() {
  useEffect(() => {
    const stored = getStoredTheme();
    if (stored) {
      document.documentElement.dataset.theme = stored;
    } else {
      // Default is dark; ensure dataset is set for CSS variables.
      document.documentElement.dataset.theme = 'dark';
    }
  }, []);

  return null;
}

