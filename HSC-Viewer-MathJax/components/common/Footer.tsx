export default function Footer() {
  return (
    <footer className="border-t border-black/10 px-4 py-4 text-sm text-[color:color-mix(in_srgb,var(--color-charcoal)_74%,white)]">
      <div className="mx-auto flex max-w-[1600px] flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
        <p>HSC-Viewer-MathJax keeps `.tex` as the single source of truth.</p>
        <p>Built with Next.js, bun, make4ht, and MathJax.</p>
      </div>
    </footer>
  );
}
