"use client";

import Link from "next/link";
import { Home, Menu } from "lucide-react";
import { APP_NAME } from "@/lib/constants";

export default function ReaderMobileTopBar({
  bookletTitle,
  onOpenMenu,
}: {
  bookletTitle: string | null;
  onOpenMenu: () => void;
}) {
  return (
    <header
      className="sticky top-0 z-20 border-b border-black/10 bg-[color:color-mix(in_srgb,var(--color-white)_92%,transparent)] px-3 py-2 backdrop-blur supports-[backdrop-filter]:bg-[color:color-mix(in_srgb,var(--color-white)_86%,transparent)] lg:hidden"
      style={{ paddingTop: "max(0.5rem, env(safe-area-inset-top))" }}
    >
      <div className="mx-auto flex w-full max-w-[1600px] items-center gap-2 sm:px-1">
        <button
          type="button"
          onClick={onOpenMenu}
          className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-black/10 bg-white text-[var(--color-purple)] shadow-sm"
          aria-label="Open booklet navigation"
          title="Open booklet navigation"
        >
          <Menu className="h-5 w-5" />
        </button>
        <div className="min-w-0 flex-1 text-center sm:text-left">
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--color-red)]">
            Active booklet
          </p>
          <p className="truncate text-sm font-semibold text-[var(--color-purple)] sm:text-base">
            {bookletTitle ?? "Booklet"}
          </p>
        </div>
        <Link
          href="/"
          className="inline-flex h-10 shrink-0 items-center justify-center gap-1.5 rounded-full border border-black/10 bg-white px-3 text-xs font-medium text-[var(--color-purple)] shadow-sm"
          aria-label={`Home – ${APP_NAME}`}
          title={`Home – ${APP_NAME}`}
        >
          <Home className="h-4 w-4" aria-hidden="true" />
          <span className="max-[380px]:sr-only">Home</span>
        </Link>
      </div>
    </header>
  );
}
