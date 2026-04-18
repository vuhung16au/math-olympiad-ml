"use client";

import Link from "next/link";
import { X } from "lucide-react";
import { BOOKLETS } from "@/lib/booklets";

export default function MobileMenu({
  isOpen,
  pathname,
  onClose,
}: {
  isOpen: boolean;
  pathname: string;
  onClose: () => void;
}) {
  return (
    <>
      <div
        className={[
          "fixed inset-0 z-30 bg-black/45 transition lg:hidden",
          isOpen ? "pointer-events-auto opacity-100" : "pointer-events-none opacity-0",
        ].join(" ")}
        onClick={onClose}
        aria-hidden="true"
      />
      <aside
        className={[
          "fixed inset-y-0 left-0 z-40 w-[min(88vw,22rem)] border-r border-black/10 bg-[var(--color-purple)] px-4 py-5 text-white shadow-2xl transition-transform duration-300 lg:hidden",
          isOpen ? "translate-x-0" : "-translate-x-full",
        ].join(" ")}
        aria-label="Mobile booklet navigation"
      >
        <div className="mb-6 flex items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-white/65">Navigate</p>
            <p className="text-lg font-semibold">HSC Booklets</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/15 bg-white/10"
            aria-label="Close navigation menu"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="space-y-2">
          {BOOKLETS.map((booklet) => {
            const isActive = pathname === `/booklets/${booklet.slug}`;

            if (!booklet.isAvailable) {
              return (
                <div
                  key={booklet.id}
                  className="rounded-2xl border border-white/10 bg-white/5 px-3 py-3 opacity-55"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-sm font-medium">{booklet.title}</span>
                    <span className="rounded-full bg-[var(--color-red)]/80 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] text-white">
                      Soon
                    </span>
                  </div>
                </div>
              );
            }

            return (
              <Link
                key={booklet.id}
                href={`/booklets/${booklet.slug}`}
                onClick={onClose}
                aria-current={isActive ? "page" : undefined}
                className={[
                  "block rounded-2xl border-l-4 px-3 py-3 text-sm font-medium transition",
                  isActive
                    ? "border-l-[var(--color-red)] bg-white text-[var(--color-purple)] ring-1 ring-white/60"
                    : "border-l-transparent bg-white/5 text-white/88 hover:bg-white/12 hover:text-white active:bg-white active:text-[var(--color-purple)]",
                ].join(" ")}
              >
                {booklet.title}
              </Link>
            );
          })}
        </nav>
      </aside>
    </>
  );
}
