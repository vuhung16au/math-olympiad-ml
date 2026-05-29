import Link from "next/link";
import { buildNotFoundMetadata, SITE_URL } from "@/lib/og-metadata";

export const metadata = buildNotFoundMetadata(SITE_URL);

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
