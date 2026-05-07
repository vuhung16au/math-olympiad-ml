export interface BookletSourceConfig {
  id: string;
  title: string;
  slug: string;
  sourceDir: string;
  entryTex: string;
  order: number;
  isAvailable: boolean;
}

export interface BookletManifestEntry extends BookletSourceConfig {
  htmlPath: string;
  assetBasePath: string;
  conversionWarnings: string[];
  lastGeneratedAt: string;
}

export interface GeneratedBookletDocument {
  slug: string;
  title: string;
  html: string;
  warningCount: number;
  conversionWarnings: string[];
  assetBasePath: string;
  lastGeneratedAt: string;
}

export interface ConversionResult {
  booklet: BookletManifestEntry;
  html: string;
}

export const BOOKLETS: BookletSourceConfig[] = [
  { id: "hsc-collections", title: "HSC Collections", slug: "hsc-collections", sourceDir: "HSC-Collections", entryTex: "HSC-Collections.tex", order: 1, isAvailable: true },
  { id: "hsc-combinatorics", title: "HSC Combinatorics", slug: "hsc-combinatorics", sourceDir: "HSC-Combinatorics", entryTex: "HSC-Combinatorics.tex", order: 2, isAvailable: true },
  { id: "hsc-common", title: "HSC Common", slug: "hsc-common", sourceDir: "HSC-Common", entryTex: "README.md", order: 3, isAvailable: false },
  { id: "hsc-complex-numbers", title: "HSC Complex Numbers", slug: "hsc-complex-numbers", sourceDir: "HSC-ComplexNumbers", entryTex: "HSC-ComplexNumbers.tex", order: 4, isAvailable: true },
  { id: "hsc-differential-equations", title: "HSC Differential Equations", slug: "hsc-differential-equations", sourceDir: "HSC-DifferentialEquations", entryTex: "HSC-DifferentialEquations.tex", order: 5, isAvailable: true },
  { id: "hsc-distributions", title: "HSC Distributions", slug: "hsc-distributions", sourceDir: "HSC-Distributions", entryTex: "HSC-Distributions.tex", order: 6, isAvailable: true },
  { id: "hsc-functions", title: "HSC Functions", slug: "hsc-functions", sourceDir: "HSC-Functions", entryTex: "HSC-Functions.tex", order: 7, isAvailable: true },
  { id: "hsc-induction", title: "HSC Induction", slug: "hsc-induction", sourceDir: "HSC-Induction", entryTex: "HSC-Induction.tex", order: 8, isAvailable: true },
  { id: "hsc-inequalities", title: "HSC Inequalities", slug: "hsc-inequalities", sourceDir: "HSC-Inequalities", entryTex: "HSC-Inequalities.tex", order: 9, isAvailable: true },
  { id: "hsc-integrals", title: "HSC Integrals", slug: "hsc-integrals", sourceDir: "HSC-Integrals", entryTex: "HSC-Integrals.tex", order: 10, isAvailable: true },
  { id: "hsc-last-resorts", title: "HSC Last Resorts", slug: "hsc-last-resorts", sourceDir: "HSC-LastResorts", entryTex: "HSC-LastResorts.tex", order: 11, isAvailable: true },
  { id: "hsc-mechanics", title: "HSC Mechanics", slug: "hsc-mechanics", sourceDir: "HSC-Mechanics", entryTex: "HSC-Mechanics.tex", order: 12, isAvailable: true },
  { id: "hsc-polynomials", title: "HSC Polynomials", slug: "hsc-polynomials", sourceDir: "HSC-Polynomials", entryTex: "HSC-Polynomials.tex", order: 13, isAvailable: true },
  { id: "hsc-polynomials-extension1", title: "HSC Polynomials Extension 1", slug: "hsc-polynomials-extension1", sourceDir: "HSC-Polynomials-Extension1", entryTex: "HSC-Polynomials-Extension1.tex", order: 14, isAvailable: true },
  { id: "hsc-probability", title: "HSC Probability", slug: "hsc-probability", sourceDir: "HSC-Probability", entryTex: "HSC-Probability.tex", order: 15, isAvailable: true },
  { id: "hsc-proofs", title: "HSC Proofs", slug: "hsc-proofs", sourceDir: "HSC-Proofs", entryTex: "HSC-Proofs.tex", order: 16, isAvailable: true },
  { id: "hsc-sequences", title: "HSC Sequences", slug: "hsc-sequences", sourceDir: "HSC-Sequences", entryTex: "HSC-Sequences.tex", order: 17, isAvailable: true },
  { id: "hsc-trigonometry", title: "HSC Trigonometry", slug: "hsc-trigonometry", sourceDir: "HSC-Trigonometry", entryTex: "HSC-Trigonometry.tex", order: 18, isAvailable: true },
  { id: "hsc-vectors", title: "HSC Vectors", slug: "hsc-vectors", sourceDir: "HSC-Vectors", entryTex: "HSC-Vectors.tex", order: 19, isAvailable: true },
];

export function getBookletBySlug(slug: string) {
  return BOOKLETS.find((booklet) => booklet.slug === slug);
}

export function getBookletBySourceDir(sourceDir: string) {
  return BOOKLETS.find((booklet) => booklet.sourceDir === sourceDir);
}

export function getVisibleBooklets<T extends { isAvailable: boolean }>(booklets: T[]) {
  return booklets.filter((booklet) => booklet.isAvailable);
}
