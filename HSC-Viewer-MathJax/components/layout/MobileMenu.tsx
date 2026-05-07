"use client";

import Link from "next/link";
import type { BookletManifestEntry } from "@/lib/booklets";

export default function MobileMenu({
  isOpen,
  pathname,
  booklets,
  onClose,
}: {
  isOpen: boolean;
  pathname: string;
  booklets: BookletManifestEntry[];
  onClose: () => void;
}) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-40 bg-black/35 lg:hidden">
      <div className="h-full w-[82vw] max-w-sm overflow-y-auto bg-[var(--color-purple)] px-4 py-6 text-white shadow-2xl">
        <div className="mb-4 flex items-center justify-between">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-white/70">
            Booklets
          </p>
          <button
            type="button"
            aria-label="Close booklet menu"
            title="Close booklet menu"
            onClick={onClose}
            className="rounded-full border border-white/20 px-3 py-1 text-sm"
          >
            Close
          </button>
        </div>
        <nav className="space-y-2">
          {booklets.map((booklet) => {
            const isActive = pathname === `/booklets/${booklet.slug}`;

            return (
              <Link
                key={booklet.slug}
                href={`/booklets/${booklet.slug}`}
                onClick={onClose}
                className={[
                  "block rounded-2xl px-3 py-3 text-sm font-medium",
                  isActive ? "bg-white text-[var(--color-purple)]" : "bg-white/8 text-white",
                ].join(" ")}
              >
                {booklet.title}
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
