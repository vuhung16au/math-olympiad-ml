import './globals.css';
import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { SiteFooter } from './components/SiteFooter';
import { ThemeInit } from './components/ThemeInit';

export const metadata: Metadata = {
  title: 'Fractals Generator',
  description: 'Interactive fractal lab built with Next.js',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" data-theme="dark">
      <body>
        <div className="app-root">
          <ThemeInit />
          <div className="app-content">{children}</div>
          <div className="site-footer-shell">
            <SiteFooter />
          </div>
        </div>
      </body>
    </html>
  );
}
