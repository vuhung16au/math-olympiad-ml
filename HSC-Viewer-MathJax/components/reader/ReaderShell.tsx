import type { GeneratedBookletDocument } from "@/lib/booklets";
import BookletContent from "@/components/reader/BookletContent";

export default function ReaderShell({
  booklet,
}: {
  booklet: GeneratedBookletDocument;
}) {
  return (
    <section className="min-h-[calc(100vh-4rem)]">
      <div className="border-b border-black/10 bg-white/75 px-4 py-4 backdrop-blur sm:px-6 lg:px-10">
        <div className="mx-auto max-w-5xl">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-red)]">
            LaTeX to HTML
          </p>
          <div className="mt-2 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-2xl font-semibold tracking-tight text-[var(--color-purple)]">
                {booklet.title}
              </h2>
              <p className="text-sm text-[color:color-mix(in_srgb,var(--color-charcoal)_76%,white)]">
                Generated {new Date(booklet.lastGeneratedAt).toLocaleString()}
              </p>
            </div>
            <p className="text-sm text-[color:color-mix(in_srgb,var(--color-charcoal)_74%,white)]">
              {booklet.warningCount > 0
                ? `${booklet.warningCount} conversion warnings recorded`
                : "No conversion warnings recorded"}
            </p>
          </div>
        </div>
      </div>
      <div className="mx-auto max-w-5xl">
        <BookletContent html={booklet.html} />
      </div>
    </section>
  );
}
