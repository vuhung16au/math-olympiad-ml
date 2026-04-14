import './globals.css';
import type { Metadata } from 'next';
import type { ReactNode } from 'react';

export const metadata: Metadata = {
  title: 'Fractals Generator',
  description: 'Interactive fractal lab built with Next.js',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <footer className="site-footer">
          <p>
            Source code available on github:{' '}
            <a href="https://github.com/vuhung16au/math-olympiad-ml/tree/main/fractals-generator">
              https://github.com/vuhung16au/math-olympiad-ml/tree/main/fractals-generator
            </a>
          </p>
          <p>Author: Vu Hung Nguyen, License: MIT</p>
        </footer>
      </body>
    </html>
  );
}
