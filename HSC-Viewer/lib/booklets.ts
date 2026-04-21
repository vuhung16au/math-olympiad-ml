export interface Booklet {
  id: string;              // e.g., "hsc-collections"
  title: string;           // Display name
  slug: string;            // URL slug
  pdfUrl: string;          // Raw GitHub URL
  thumbnailPath: string;   // Local path to thumbnail
  isAvailable: boolean;    // false for HSC-Sequences
  comingSoon?: boolean;
}

const GITHUB_RAW_URL = 'https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main';

export const BOOKLETS: Booklet[] = [
  {
    id: "hsc-collections",
    title: "HSC Collections",
    slug: "hsc-collections",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Collections/releases/HSC-Collections.pdf`,
    thumbnailPath: "/thumbnails/hsc-collections.png",
    isAvailable: true,
  },
  {
    id: "hsc-combinatorics",
    title: "HSC Combinatorics",
    slug: "hsc-combinatorics",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Combinatorics/releases/HSC-Combinatorics.pdf`,
    thumbnailPath: "/thumbnails/hsc-combinatorics.png",
    isAvailable: true,
  },
  {
    id: "hsc-complex-numbers",
    title: "HSC Complex Numbers",
    slug: "hsc-complex-numbers",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-ComplexNumbers/releases/HSC-ComplexNumbers.pdf`,
    thumbnailPath: "/thumbnails/hsc-complex-numbers.png",
    isAvailable: true,
  },
  {
    id: "hsc-distributions",
    title: "HSC Distributions",
    slug: "hsc-distributions",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Distributions/releases/HSC-Distributions.pdf`,
    thumbnailPath: "/thumbnails/hsc-distributions.png",
    isAvailable: true,
  },
  {
    id: "hsc-functions",
    title: "HSC Functions",
    slug: "hsc-functions",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Functions/releases/HSC-Functions.pdf`,
    thumbnailPath: "/thumbnails/hsc-functions.png",
    isAvailable: true,
  },
  {
    id: "hsc-induction",
    title: "HSC Induction",
    slug: "hsc-induction",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Induction/releases/HSC-Induction.pdf`,
    thumbnailPath: "/thumbnails/hsc-induction.png",
    isAvailable: true,
  },
  {
    id: "hsc-inequalities",
    title: "HSC Inequalities",
    slug: "hsc-inequalities",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Inequalities/releases/HSC-Inequalities.pdf`,
    thumbnailPath: "/thumbnails/hsc-inequalities.png",
    isAvailable: true,
  },
  {
    id: "hsc-integrals",
    title: "HSC Integrals",
    slug: "hsc-integrals",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Integrals/releases/HSC-Integrals.pdf`,
    thumbnailPath: "/thumbnails/hsc-integrals.png",
    isAvailable: true,
  },
  {
    id: "hsc-last-resorts",
    title: "HSC Last Resorts",
    slug: "hsc-last-resorts",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-LastResorts/releases/HSC-LastResorts.pdf`,
    thumbnailPath: "/thumbnails/hsc-last-resorts.png",
    isAvailable: true,
  },
  {
    id: "hsc-math-extension-2-book",
    title: "HSC Math Extension 2 Book",
    slug: "hsc-math-extension-2-book",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Math-Extension-2-Book/releases/HSC-Math-Extension-2-Book.pdf`,
    thumbnailPath: "/thumbnails/hsc-math-extension-2-book.png",
    isAvailable: true,
  },
  {
    id: "hsc-mechanics",
    title: "HSC Mechanics",
    slug: "hsc-mechanics",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Mechanics/releases/HSC-Mechanics.pdf`,
    thumbnailPath: "/thumbnails/hsc-mechanics.png",
    isAvailable: true,
  },
  {
    id: "hsc-polynomials",
    title: "HSC Polynomials",
    slug: "hsc-polynomials",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Polynomials/releases/HSC-Polynomials.pdf`,
    thumbnailPath: "/thumbnails/hsc-polynomials.png",
    isAvailable: true,
  },
  {
    id: "hsc-polynomials-extension1",
    title: "HSC Polynomials Extension 1",
    slug: "hsc-polynomials-extension1",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Polynomials-Extension1/releases/HSC-Polynomials-Extension1.pdf`,
    thumbnailPath: "/thumbnails/hsc-polynomials-extension1.png",
    isAvailable: true,
  },
  {
    id: "hsc-probability",
    title: "HSC Probability",
    slug: "hsc-probability",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Probability/releases/HSC-Probability.pdf`,
    thumbnailPath: "/thumbnails/hsc-probability.png",
    isAvailable: true,
  },
  {
    id: "hsc-proofs",
    title: "HSC Proofs",
    slug: "hsc-proofs",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Proofs/releases/HSC-Proofs.pdf`,
    thumbnailPath: "/thumbnails/hsc-proofs.png",
    isAvailable: true,
  },
  {
    id: "hsc-sequences",
    title: "HSC Sequences",
    slug: "hsc-sequences",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Sequences/releases/HSC-Sequences.pdf`,
    thumbnailPath: "/thumbnails/hsc-sequences.png",
    isAvailable: true,
  },
  {
    id: "hsc-trigonometry",
    title: "HSC Trigonometry",
    slug: "hsc-trigonometry",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Trigonometry/releases/HSC-Trigonometry.pdf`,
    thumbnailPath: "/thumbnails/hsc-trigonometry.png",
    isAvailable: true,
  },
  {
    id: "hsc-vectors",
    title: "HSC Vectors",
    slug: "hsc-vectors",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Vectors/releases/HSC-Vectors.pdf`,
    thumbnailPath: "/thumbnails/hsc-vectors.png",
    isAvailable: true,
  },
];

export function getBookletBySlug(slug: string): Booklet | undefined {
  return BOOKLETS.find(b => b.slug === slug);
}

export function getAvailableBooklets(): Booklet[] {
  return BOOKLETS.filter(b => b.isAvailable);
}
