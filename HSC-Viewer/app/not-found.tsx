import type { Metadata } from "next";
import Link from "next/link";

const SITE_URL = "https://hsc-math-hub.vercel.app";

export const metadata: Metadata = {
  title: "Page not found — HSC Math Hub",
  description: "This page does not exist. Browse booklets on HSC Math Hub.",
  openGraph: {
    title: "Page not found — HSC Math Hub",
    description: "This page does not exist. Browse booklets on HSC Math Hub.",
    url: SITE_URL,
    type: "website",
    siteName: "HSC Math Hub",
    images: [
      {
        url: `${SITE_URL}/og/site-fallback.png`,
        width: 1200,
        height: 630,
      },
    ],
  },
};

export default function NotFound() {
  return (
    <main className="mx-auto max-w-[720px] px-5 py-12">
      <h1 className="text-balance text-3xl font-semibold text-[var(--color-purple)]">
        Page not found
      </h1>
      <p className="mt-3 text-pretty text-base leading-7 text-[color:color-mix(in_srgb,var(--color-charcoal)_78%,white)]">
        This page does not exist.
      </p>
      <div className="mt-6">
        <Link
          href="/"
          title="Go to home"
          className="inline-flex items-center rounded-full bg-[var(--color-purple)] px-5 py-2.5 text-sm font-medium text-white"
        >
          Go to home
        </Link>
      </div>
    </main>
  );
}

