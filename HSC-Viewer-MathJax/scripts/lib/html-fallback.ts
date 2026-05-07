import type { BookletSourceConfig } from "@/lib/booklets";

function escapeHtml(content: string) {
  return content
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

export function buildFallbackHtml(
  booklet: BookletSourceConfig,
  message: string,
  sourcePreview: string,
) {
  return `
    <article class="booklet-document">
      <header class="fallback-hero">
        <p class="eyebrow">Generated fallback</p>
        <h1>${booklet.title}</h1>
        <p>This booklet could not be converted cleanly to HTML yet. The LaTeX source remains the single source of truth.</p>
      </header>
      <section class="callout warning">
        <h2>Conversion note</h2>
        <p>${escapeHtml(message)}</p>
      </section>
      <section>
        <h2>Source preview</h2>
        <pre><code>${escapeHtml(sourcePreview)}</code></pre>
      </section>
    </article>
  `.trim();
}
