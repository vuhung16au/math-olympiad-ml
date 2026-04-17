"use client";

import Link from "next/link";
import { Menu, Github, ExternalLink } from "lucide-react";
import { APP_NAME, REPO_LINKS } from "@/lib/constants";

export default function Header({
  currentTitle,
  onOpenMenu,
}: {
  currentTitle: string | null;
  onOpenMenu: () => void;
}) {
  return (
    <header className="sticky top-0 z-20 border-b border-black/10 bg-[color:color-mix(in_srgb,var(--color-white)_86%,transparent)] backdrop-blur">
      <div className="mx-auto flex h-16 w-full max-w-[1600px] items-center gap-4 px-4 sm:px-6 lg:px-8">
        <button
          type="button"
          onClick={onOpenMenu}
          className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-black/10 bg-white text-[var(--color-purple)] shadow-sm lg:hidden"
          aria-label="Open navigation menu"
        >
          <Menu className="h-5 w-5" />
        </button>

        <Link href="/" className="flex min-w-0 items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[var(--color-purple)] text-sm font-semibold text-white shadow-sm">
            HSC
          </div>
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold uppercase tracking-[0.24em] text-[var(--color-red)]">
              Mathematics Hub
            </p>
            <p className="truncate text-base font-semibold text-[var(--color-purple)]">
              {APP_NAME}
            </p>
          </div>
        </Link>

        <div className="hidden min-w-0 flex-1 items-center justify-center lg:flex">
          <div className="truncate rounded-full border border-black/8 bg-white px-4 py-2 text-sm text-[var(--color-charcoal)] shadow-sm">
            {currentTitle ? `Viewing ${currentTitle}` : "Browse the HSC booklet library"}
          </div>
        </div>

        <div className="ml-auto flex items-center gap-2 sm:gap-3">
          <a
            href={REPO_LINKS.github}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-[var(--color-purple)] shadow-sm hover:border-[var(--color-purple)]"
          >
            <Github className="h-4 w-4" />
            <span className="hidden sm:inline">Repository</span>
          </a>
          <a
            href={REPO_LINKS.linkedin}
            target="_blank"
            rel="noreferrer"
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-black/10 bg-white text-[var(--color-red)] shadow-sm hover:border-[var(--color-red)]"
            aria-label="Open LinkedIn profile"
          >
            <ExternalLink className="h-4 w-4" />
          </a>
        </div>
      </div>
    </header>
  );
}
