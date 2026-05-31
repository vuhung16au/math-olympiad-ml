export interface Booklet {
  id: string;              // e.g., "hsc-collections"
  title: string;           // Display name
  slug: string;            // URL slug
  pdfUrl: string;          // Raw GitHub URL
  thumbnailPath: string;   // Local path to thumbnail
  description: string;
  pageCount: number;
  isAvailable: boolean;    // false: no link / reader; shows Soon in nav and home grid
  comingSoon?: boolean;
}

const GITHUB_RAW_URL = 'https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main';

export const BOOKLETS: Booklet[] = [
  {
    id: "hsc-sequences",
    title: "HSC Sequences",
    slug: "hsc-sequences",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Sequences/releases/HSC-Sequences.pdf`,
    thumbnailPath: "/thumbnails/hsc-math-extension-2-book.png",
    description: "Sequences and series techniques for HSC Mathematics, with worked examples and problem-solving strategies.",
    pageCount: 51,
    isAvailable: true,
  },
  {
    id: "hsc-trigonometry",
    title: "HSC Trigonometry",
    slug: "hsc-trigonometry",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Trigonometry/releases/HSC-Trigonometry.pdf`,
    thumbnailPath: "/thumbnails/hsc-trigonometry.png",
    description: "Core trigonometry for HSC Mathematics: identities, equations, graphs, and applications with worked examples.",
    pageCount: 66,
    isAvailable: true,
  },
  {
    id: "hsc-combinatorics",
    title: "HSC Combinatorics",
    slug: "hsc-combinatorics",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Combinatorics/releases/HSC-Combinatorics.pdf`,
    thumbnailPath: "/thumbnails/hsc-combinatorics.png",
    description: "Counting principles, permutations and combinations, and classic combinatorics problems for HSC prep.",
    pageCount: 82,
    isAvailable: true,
  },
  {
    id: "hsc-differential-equations",
    title: "HSC Differential Equations",
    slug: "hsc-differential-equations",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-DifferentialEquations/releases/HSC-DifferentialEquations.pdf`,
    thumbnailPath: "/thumbnails/hsc-differential-equations.png",
    description: "Differential equations for HSC Mathematics: methods, modeling, and applications with step-by-step solutions.",
    pageCount: 117,
    isAvailable: true,
  },
  {
    id: "hsc-functions",
    title: "HSC Functions",
    slug: "hsc-functions",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Functions/releases/HSC-Functions.pdf`,
    thumbnailPath: "/thumbnails/hsc-functions.png",
    description: "Functions for HSC Mathematics: transformations, inverses, composition, and key problem-solving techniques.",
    pageCount: 66,
    isAvailable: true,
  },
  {
    id: "hsc-distributions",
    title: "HSC Distributions",
    slug: "hsc-distributions",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Distributions/releases/HSC-Distributions.pdf`,
    thumbnailPath: "/thumbnails/hsc-distributions.png",
    description: "Probability distributions for HSC Mathematics: discrete and continuous models, properties, and examples.",
    pageCount: 54,
    isAvailable: true,
  },
  {
    id: "hsc-polynomials-extension1",
    title: "HSC Polys Ext 1",
    slug: "hsc-polynomials-extension1",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Polynomials-Extension1/releases/HSC-Polynomials-Extension1.pdf`,
    thumbnailPath: "/thumbnails/hsc-polynomials-extension1.png",
    description: "Polynomials for HSC Extension 1: factorisation, remainder theorem, graphs, and algebraic techniques.",
    pageCount: 70,
    isAvailable: true,
  },
  {
    id: "hsc-probability",
    title: "HSC Probability",
    slug: "hsc-probability",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Probability/releases/HSC-Probability.pdf`,
    thumbnailPath: "/thumbnails/hsc-probability.png",
    description: "Probability for HSC Mathematics: events, conditional probability, independence, and common exam-style problems.",
    pageCount: 74,
    isAvailable: true,
  },
  {
    id: "hsc-proofs",
    title: "HSC Proofs",
    slug: "hsc-proofs",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Proofs/releases/HSC-Proofs.pdf`,
    thumbnailPath: "/thumbnails/hsc-proofs.png",
    description: "Proof techniques for HSC Mathematics: structure, rigor, and strategies with worked proof examples.",
    pageCount: 76,
    isAvailable: true,
  },
  {
    id: "hsc-polynomials",
    title: "HSC Polynomials",
    slug: "hsc-polynomials",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Polynomials/releases/HSC-Polynomials.pdf`,
    thumbnailPath: "/thumbnails/hsc-polynomials.png",
    description: "Polynomials for HSC Mathematics: algebraic manipulation, graph features, and problem-solving approaches.",
    pageCount: 53,
    isAvailable: true,
  },
  {
    id: "hsc-induction",
    title: "HSC Induction",
    slug: "hsc-induction",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Induction/releases/HSC-Induction.pdf`,
    thumbnailPath: "/thumbnails/hsc-induction.png",
    description: "Mathematical induction for HSC Extension: patterns, inequalities, divisibility, and proof practice problems.",
    pageCount: 41,
    isAvailable: true,
  },
  {
    id: "hsc-inequalities",
    title: "HSC Inequalities",
    slug: "hsc-inequalities",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Inequalities/releases/HSC-Inequalities.pdf`,
    thumbnailPath: "/thumbnails/hsc-inequalities.png",
    description: "Inequalities for HSC Mathematics: common techniques, classic results, and worked examples.",
    pageCount: 75,
    isAvailable: true,
  },
  {
    id: "hsc-complex-numbers",
    title: "HSC Complex Numbers",
    slug: "hsc-complex-numbers",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-ComplexNumbers/releases/HSC-ComplexNumbers.pdf`,
    thumbnailPath: "/thumbnails/hsc-complex-numbers.png",
    description: "Complex numbers for HSC Mathematics: algebra, geometry, modulus-argument form, and applications.",
    pageCount: 68,
    isAvailable: true,
  },
  {
    id: "hsc-integrals",
    title: "HSC Integrals",
    slug: "hsc-integrals",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Integrals/releases/HSC-Integrals.pdf`,
    thumbnailPath: "/thumbnails/hsc-integrals.png",
    description: "Integration for HSC Mathematics: techniques, applications, and exam-style problems with worked solutions.",
    pageCount: 82,
    isAvailable: true,
  },
  {
    id: "hsc-mechanics",
    title: "HSC Mechanics",
    slug: "hsc-mechanics",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Mechanics/releases/HSC-Mechanics.pdf`,
    thumbnailPath: "/thumbnails/hsc-mechanics.png",
    description: "Mechanics for HSC Mathematics: vectors, motion, forces, and modeling with worked examples.",
    pageCount: 85,
    isAvailable: true,
  },
  {
    id: "hsc-vectors",
    title: "HSC Vectors",
    slug: "hsc-vectors",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Vectors/releases/HSC-Vectors.pdf`,
    thumbnailPath: "/thumbnails/hsc-vectors.png",
    description: "Vectors for HSC Mathematics: geometric and algebraic methods, lines and planes, and problem-solving practice.",
    pageCount: 72,
    isAvailable: true,
  },
  {
    id: "hsc-collections",
    title: "HSC Collections",
    slug: "hsc-collections",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Collections/releases/HSC-Collections.pdf`,
    thumbnailPath: "/thumbnails/hsc-collections.png",
    description: "A curated collection of HSC Mathematics problems and solutions across key topics and techniques.",
    pageCount: 52,
    isAvailable: true,
  },
  {
    id: "hsc-last-resorts",
    title: "HSC Last Resorts",
    slug: "hsc-last-resorts",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-LastResorts/releases/HSC-LastResorts.pdf`,
    thumbnailPath: "/thumbnails/hsc-last-resorts.png",
    description: "Challenging HSC Mathematics problems with creative techniques and detailed worked solutions.",
    pageCount: 117,
    isAvailable: true,
  },
  {
    id: "hsc-math-extension-2-book",
    title: "HSC MX2 Full",
    slug: "hsc-math-extension-2-book",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Math-Extension-2-Book/releases/HSC-Math-Extension-2-Book.pdf`,
    thumbnailPath: "/thumbnails/hsc-math-extension-2-book.png",
    description: "Full HSC Mathematics Extension 2 booklet (coming soon).",
    pageCount: 0,
    isAvailable: false,
  },
];

export function getBookletBySlug(slug: string): Booklet | undefined {
  return BOOKLETS.find(b => b.slug === slug);
}

export function getAvailableBooklets(): Booklet[] {
  return BOOKLETS.filter(b => b.isAvailable);
}

export function isValidBookletPage(booklet: Booklet, page: number): boolean {
  return Number.isSafeInteger(page) && page >= 1 && page <= booklet.pageCount;
}
