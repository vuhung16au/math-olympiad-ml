import Link from "next/link";

export default function NotFoundPage() {
  return (
    <section className="px-4 py-10 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-2xl rounded-[2rem] border border-black/10 bg-white/75 p-8 text-center shadow-lg">
        <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[var(--color-red)]">
          Not Found
        </p>
        <h2 className="mt-4 text-3xl font-semibold text-[var(--color-purple)]">
          This booklet page does not exist yet.
        </h2>
        <p className="mt-3 text-[color:color-mix(in_srgb,var(--color-charcoal)_76%,white)]">
          Regenerate the booklet HTML and try again.
        </p>
        <Link
          href="/"
          className="mt-6 inline-flex rounded-full bg-[var(--color-purple)] px-5 py-3 text-sm font-semibold text-white"
        >
          Back to home
        </Link>
      </div>
    </section>
  );
}
