import Link from "next/link";
import { getVisibleBooklets } from "@/lib/booklets";
import { getGeneratedManifest } from "@/lib/generated-content";

export default async function HomePage() {
  const manifest = getVisibleBooklets(await getGeneratedManifest());

  return (
    <section className="px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-5xl rounded-[2rem] border border-black/10 bg-white/70 p-8 shadow-[0_24px_80px_rgba(60,16,83,0.08)] backdrop-blur">
        <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-red)]">
          HSC Viewer MathJax
        </p>
        <h2 className="mt-4 text-4xl font-semibold tracking-tight text-[var(--color-purple)] sm:text-5xl">
          Browse HSC booklet content online from the original LaTeX projects.
        </h2>
        <p className="mt-4 max-w-3xl text-base leading-7 text-[color:color-mix(in_srgb,var(--color-charcoal)_84%,white)] sm:text-lg">
          This viewer generates web-readable HTML from the root `HSC-xxx` source folders. The
          `.tex` files stay untouched and remain the only authored source.
        </p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {manifest.map((booklet) => (
            <Link
              key={booklet.slug}
              href={`/booklets/${booklet.slug}`}
              className="rounded-3xl border border-black/10 bg-[color:color-mix(in_srgb,var(--color-ivory)_88%,white)] p-5 transition hover:-translate-y-0.5 hover:border-[var(--color-purple)]/25 hover:shadow-lg"
            >
              <p className="text-sm font-semibold text-[var(--color-purple)]">{booklet.title}</p>
              <p className="mt-2 text-sm leading-6 text-[color:color-mix(in_srgb,var(--color-charcoal)_74%,white)]">
                Open the generated HTML reader for this booklet.
              </p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
