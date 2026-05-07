import Link from "next/link";
import type { BookletManifestEntry } from "@/lib/booklets";

export default function Sidebar({
  pathname,
  booklets,
}: {
  pathname: string;
  booklets: BookletManifestEntry[];
}) {
  return (
    <aside className="sticky top-0 hidden h-screen w-[var(--sidebar-width)] shrink-0 overflow-y-auto border-r border-black/10 bg-[color:color-mix(in_srgb,var(--color-purple)_94%,white)] px-4 py-6 text-white lg:block">
      <div className="mb-5 px-3">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-white/70">
          Booklets
        </p>
      </div>
      <nav className="space-y-1.5" aria-label="Booklet navigation">
        {booklets.map((booklet) => {
          const isActive = pathname === `/booklets/${booklet.slug}`;

          return (
            <Link
              key={booklet.slug}
              href={`/booklets/${booklet.slug}`}
              aria-current={isActive ? "page" : undefined}
              className={[
                "group flex items-center rounded-2xl border-l-4 px-3 py-3 text-sm font-medium transition",
                isActive
                  ? "border-l-[var(--color-red)] bg-white text-[var(--color-purple)] shadow-md ring-1 ring-white/60"
                  : "border-l-transparent text-white/84 hover:bg-white/10 hover:text-white",
              ].join(" ")}
            >
              <span className="truncate">{booklet.title}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
