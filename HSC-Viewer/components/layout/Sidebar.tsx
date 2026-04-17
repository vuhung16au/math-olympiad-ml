import Link from "next/link";
import { BOOKLETS } from "@/lib/booklets";

export default function Sidebar({ pathname }: { pathname: string }) {
  return (
    <aside className="sticky top-16 hidden h-[calc(100vh-4rem)] w-[var(--sidebar-width)] shrink-0 overflow-y-auto border-r border-black/10 bg-[color:color-mix(in_srgb,var(--color-purple)_92%,white)] px-4 py-6 text-white lg:block">
      <p className="mb-4 px-3 text-xs font-semibold uppercase tracking-[0.24em] text-white/70">
        Booklets
      </p>
      <nav className="space-y-1.5" aria-label="Booklet navigation">
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
              className={[
                "group flex items-center rounded-2xl px-3 py-3 text-sm font-medium transition",
                isActive
                  ? "bg-white text-[var(--color-purple)] shadow-sm"
                  : "text-white/84 hover:bg-white/10 hover:text-white",
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
