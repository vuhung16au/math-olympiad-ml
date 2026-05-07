"use client";

import { Menu } from "lucide-react";

export default function Header({
  title,
  onOpenMenu,
}: {
  title: string;
  onOpenMenu: () => void;
}) {
  return (
    <header className="sticky top-0 z-30 border-b border-black/10 bg-[color:color-mix(in_srgb,var(--color-white)_72%,transparent)] backdrop-blur">
      <div className="mx-auto flex h-16 max-w-[1600px] items-center justify-between px-4 sm:px-6">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-red)]">
            HSC Viewer MathJax
          </p>
          <h1 className="text-lg font-semibold text-[var(--color-purple)]">{title}</h1>
        </div>
        <button
          type="button"
          title="Open booklet menu"
          aria-label="Open booklet menu"
          onClick={onOpenMenu}
          className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-black/10 bg-white/70 text-[var(--color-purple)] lg:hidden"
        >
          <Menu className="h-5 w-5" />
        </button>
      </div>
    </header>
  );
}
