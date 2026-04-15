'use client';

import { useEffect, useState } from 'react';
import { getStoredTheme, setTheme, type ThemeMode } from './ThemeInit';

function IconMoon() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
      <path
        fill="currentColor"
        d="M12.7 2.1c.3 0 .5.2.5.5 0 .2-.1.4-.3.5A7.5 7.5 0 0 0 16.9 17a7.3 7.3 0 0 0 4-.9c.2-.1.5 0 .6.2.1.2.1.5-.1.7A9.6 9.6 0 0 1 12 21.5 9.5 9.5 0 0 1 12.7 2.1z"
      />
    </svg>
  );
}

function IconSun() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
      <path
        fill="currentColor"
        d="M12 18.2A6.2 6.2 0 1 1 12 5.8a6.2 6.2 0 0 1 0 12.4zm0-1.8a4.4 4.4 0 1 0 0-8.8 4.4 4.4 0 0 0 0 8.8zM12 2.2c.5 0 .9.4.9.9v1.5a.9.9 0 1 1-1.8 0V3.1c0-.5.4-.9.9-.9zm0 17.6c.5 0 .9.4.9.9v1.5a.9.9 0 1 1-1.8 0v-1.5c0-.5.4-.9.9-.9zM4.3 5.6c.3-.3.9-.3 1.2 0l1.1 1.1a.9.9 0 1 1-1.2 1.2L4.3 6.8a.9.9 0 0 1 0-1.2zm12.3 12.3c.3-.3.9-.3 1.2 0l1.1 1.1a.9.9 0 1 1-1.2 1.2l-1.1-1.1a.9.9 0 0 1 0-1.2zM2.2 12c0-.5.4-.9.9-.9h1.5a.9.9 0 1 1 0 1.8H3.1c-.5 0-.9-.4-.9-.9zm17.6 0c0-.5.4-.9.9-.9h1.5a.9.9 0 1 1 0 1.8h-1.5c-.5 0-.9-.4-.9-.9zM5.6 19.7c-.3-.3-.3-.9 0-1.2l1.1-1.1a.9.9 0 1 1 1.2 1.2l-1.1 1.1c-.3.3-.9.3-1.2 0zm12.3-12.3c-.3-.3-.3-.9 0-1.2l1.1-1.1a.9.9 0 1 1 1.2 1.2l-1.1 1.1c-.3.3-.9.3-1.2 0z"
      />
    </svg>
  );
}

export function ThemeToggle() {
  const [mode, setMode] = useState<ThemeMode>('dark');

  useEffect(() => {
    const stored = getStoredTheme();
    if (stored) setMode(stored);
  }, []);

  const nextMode: ThemeMode = mode === 'dark' ? 'light' : 'dark';

  return (
    <button
      type="button"
      className="icon-button"
      onClick={() => {
        setTheme(nextMode);
        setMode(nextMode);
      }}
      aria-label={`Switch to ${nextMode} mode`}
      title={`Switch to ${nextMode} mode`}
    >
      {mode === 'dark' ? <IconSun /> : <IconMoon />}
    </button>
  );
}

