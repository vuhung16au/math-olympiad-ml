import { BOOKLETS } from "@/lib/booklets";
import ThumbnailCard from "@/components/ui/ThumbnailCard";

export default function GridView() {
  return (
    <section className="px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
      <div className="mx-auto max-w-[1200px]">
        <div className="mb-8 max-w-3xl">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-red)]">
            HSC Viewer
          </p>
          <h1 className="text-4xl font-semibold tracking-tight text-[var(--color-purple)] sm:text-5xl">
            Browse the booklet collection and open any chapter directly in the browser.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-[color:color-mix(in_srgb,var(--color-charcoal)_82%,white)] sm:text-lg">
            Browse every released booklet from one place. The grid is ready for generated cover thumbnails, and each available title opens in an in-browser PDF reader.
          </p>
        </div>

        <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {BOOKLETS.map((booklet) => (
            <ThumbnailCard key={booklet.id} booklet={booklet} />
          ))}
        </div>
      </div>
    </section>
  );
}
