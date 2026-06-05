export interface Booklet {
  id: string;              // e.g., "hsc-collections"
  title: string;           // Display name
  slug: string;            // URL slug
  pdfUrl: string;          // Raw GitHub URL
  thumbnailPath: string;   // Local path to thumbnail
  cardBlurb: string;       // Short one-liner on home grid cards (~8–12 words)
  description: string;     // SEO / Open Graph meta (~150–165 characters)
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
    cardBlurb: "Arithmetic and geometric series, sigma notation, and recurrence relations.",
    description:
      "HSC Sequences booklet — arithmetic and geometric series, sigma notation, and recurrence relations with worked examples. Free HSC Maths revision on HSC Math Hub.",
    pageCount: 51,
    isAvailable: true,
  },
  {
    id: "hsc-trigonometry",
    title: "HSC Trigonometry",
    slug: "hsc-trigonometry",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Trigonometry/releases/HSC-Trigonometry.pdf`,
    thumbnailPath: "/thumbnails/hsc-trigonometry.png",
    cardBlurb: "Identities, trig equations, graphs, and inverse functions.",
    description:
      "HSC Trigonometry booklet for Extension 1 and 2 — identities, equations, graphs, and inverse trig with worked examples. Read free on HSC Math Hub.",
    pageCount: 66,
    isAvailable: true,
  },
  {
    id: "hsc-combinatorics",
    title: "HSC Combinatorics",
    slug: "hsc-combinatorics",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Combinatorics/releases/HSC-Combinatorics.pdf`,
    thumbnailPath: "/thumbnails/hsc-combinatorics.png",
    cardBlurb: "Counting, permutations, combinations, and classic Extension 2 problems.",
    description:
      "HSC Combinatorics booklet — counting principles, permutations, combinations, and Extension 2 problems with worked solutions. Free on HSC Math Hub.",
    pageCount: 82,
    isAvailable: true,
  },
  {
    id: "hsc-differential-equations",
    title: "HSC Differential Equations",
    slug: "hsc-differential-equations",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-DifferentialEquations/releases/HSC-DifferentialEquations.pdf`,
    thumbnailPath: "/thumbnails/hsc-differential-equations.png",
    cardBlurb: "First-order ODEs, modelling, and step-by-step Extension 2 solutions.",
    description:
      "HSC Differential Equations booklet — methods, modelling, and applications with step-by-step worked solutions for Extension 2. Read free on HSC Math Hub.",
    pageCount: 117,
    isAvailable: true,
  },
  {
    id: "hsc-functions",
    title: "HSC Functions",
    slug: "hsc-functions",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Functions/releases/HSC-Functions.pdf`,
    thumbnailPath: "/thumbnails/hsc-functions.png",
    cardBlurb: "Transformations, inverses, composition, and function sketching.",
    description:
      "HSC Functions booklet — transformations, inverses, composition, and sketching with worked examples for Extension 1 and 2. Free online on HSC Math Hub.",
    pageCount: 66,
    isAvailable: true,
  },
  {
    id: "hsc-distributions",
    title: "HSC Distributions",
    slug: "hsc-distributions",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Distributions/releases/HSC-Distributions.pdf`,
    thumbnailPath: "/thumbnails/hsc-distributions.png",
    cardBlurb: "Discrete and continuous probability distributions for Extension 1 and 2.",
    description:
      "HSC Distributions booklet — discrete and continuous probability models, properties, and worked examples. Free HSC Maths revision on HSC Math Hub.",
    pageCount: 54,
    isAvailable: true,
  },
  {
    id: "hsc-polynomials-extension1",
    title: "HSC Polys Ext 1",
    slug: "hsc-polynomials-extension1",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Polynomials-Extension1/releases/HSC-Polynomials-Extension1.pdf`,
    thumbnailPath: "/thumbnails/hsc-polynomials-extension1.png",
    cardBlurb: "Factorisation, remainder theorem, and polynomial graphs for Ext 1.",
    description:
      "HSC Extension 1 Polynomials booklet — factorisation, remainder theorem, graphs, and algebraic techniques with worked examples. Read free on HSC Math Hub.",
    pageCount: 70,
    isAvailable: true,
  },
  {
    id: "hsc-probability",
    title: "HSC Probability",
    slug: "hsc-probability",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Probability/releases/HSC-Probability.pdf`,
    thumbnailPath: "/thumbnails/hsc-probability.png",
    cardBlurb: "Conditional probability, independence, and exam-style questions.",
    description:
      "HSC Probability booklet — events, conditional probability, independence, and common exam-style problems with solutions. Free on HSC Math Hub.",
    pageCount: 74,
    isAvailable: true,
  },
  {
    id: "hsc-proofs",
    title: "HSC Proofs",
    slug: "hsc-proofs",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Proofs/releases/HSC-Proofs.pdf`,
    thumbnailPath: "/thumbnails/hsc-proofs.png",
    cardBlurb: "Proof structure, clear reasoning, and worked examples.",
    description:
      "HSC Proofs booklet — proof structure, rigour, and strategies with worked examples for Extension 1 and 2. Read free on HSC Math Hub.",
    pageCount: 76,
    isAvailable: true,
  },
  {
    id: "hsc-polynomials",
    title: "HSC Polynomials",
    slug: "hsc-polynomials",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Polynomials/releases/HSC-Polynomials.pdf`,
    thumbnailPath: "/thumbnails/hsc-polynomials.png",
    cardBlurb: "Algebra, roots, and graph features for harder polynomial work.",
    description:
      "HSC Polynomials booklet — algebraic manipulation, roots, and graph features with problem-solving approaches and worked solutions. Free on HSC Math Hub.",
    pageCount: 53,
    isAvailable: true,
  },
  {
    id: "hsc-induction",
    title: "HSC Induction",
    slug: "hsc-induction",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Induction/releases/HSC-Induction.pdf`,
    thumbnailPath: "/thumbnails/hsc-induction.png",
    cardBlurb: "Mathematical induction for inequalities, divisibility, and proofs.",
    description:
      "HSC Mathematical Induction booklet — patterns, inequalities, divisibility, and proof practice for Extension 1. Read free on HSC Math Hub.",
    pageCount: 41,
    isAvailable: true,
  },
  {
    id: "hsc-inequalities",
    title: "HSC Inequalities",
    slug: "hsc-inequalities",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Inequalities/releases/HSC-Inequalities.pdf`,
    thumbnailPath: "/thumbnails/hsc-inequalities.png",
    cardBlurb: "Classic inequality techniques and results for Extension 2.",
    description:
      "HSC Inequalities booklet — common techniques, classic results, and worked examples for Extension 2 preparation. Free online on HSC Math Hub.",
    pageCount: 75,
    isAvailable: true,
  },
  {
    id: "hsc-complex-numbers",
    title: "HSC Complex Numbers",
    slug: "hsc-complex-numbers",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-ComplexNumbers/releases/HSC-ComplexNumbers.pdf`,
    thumbnailPath: "/thumbnails/hsc-complex-numbers.png",
    cardBlurb: "Algebra, geometry, and modulus–argument form in the complex plane.",
    description:
      "HSC Complex Numbers booklet — algebra, geometry, modulus–argument form, and applications with worked examples. Read free on HSC Math Hub.",
    pageCount: 68,
    isAvailable: true,
  },
  {
    id: "hsc-integrals",
    title: "HSC Integrals",
    slug: "hsc-integrals",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Integrals/releases/HSC-Integrals.pdf`,
    thumbnailPath: "/thumbnails/hsc-integrals.png",
    cardBlurb: "Integration techniques and applications with full worked solutions.",
    description:
      "HSC Integrals booklet — integration techniques, applications, and exam-style problems with step-by-step worked solutions. Free on HSC Math Hub.",
    pageCount: 82,
    isAvailable: true,
  },
  {
    id: "hsc-mechanics",
    title: "HSC Mechanics",
    slug: "hsc-mechanics",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Mechanics/releases/HSC-Mechanics.pdf`,
    thumbnailPath: "/thumbnails/hsc-mechanics.png",
    cardBlurb: "Vectors, motion, forces, and mechanics modelling for Extension 2.",
    description:
      "HSC Mechanics booklet for Extension 2 — vectors, motion, forces, and modelling with worked examples. Read free on HSC Math Hub.",
    pageCount: 85,
    isAvailable: true,
  },
  {
    id: "hsc-vectors",
    title: "HSC Vectors",
    slug: "hsc-vectors",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Vectors/releases/HSC-Vectors.pdf`,
    thumbnailPath: "/thumbnails/hsc-vectors.png",
    cardBlurb: "Lines, planes, dot and cross products, and 3D geometry.",
    description:
      "HSC Vectors booklet — geometric and algebraic methods, lines, planes, and 3D problems with worked solutions. Free on HSC Math Hub.",
    pageCount: 72,
    isAvailable: true,
  },
  {
    id: "hsc-collections",
    title: "HSC Collections",
    slug: "hsc-collections",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Collections/releases/HSC-Collections.pdf`,
    thumbnailPath: "/thumbnails/hsc-collections.png",
    cardBlurb: "Mixed-topic problems and solutions across the HSC Maths course.",
    description:
      "HSC Collections — curated problems and solutions across key HSC Maths topics and techniques. Ideal for revision. Read free on HSC Math Hub.",
    pageCount: 57,
    isAvailable: true,
  },
  {
    id: "hsc-last-resorts",
    title: "HSC Last Resorts",
    slug: "hsc-last-resorts",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-LastResorts/releases/HSC-LastResorts.pdf`,
    thumbnailPath: "/thumbnails/hsc-last-resorts.png",
    cardBlurb: "Harder problems and creative techniques when usual methods stall.",
    description:
      "HSC Last Resorts booklet — challenging problems with creative techniques and detailed worked solutions for Extension 2. Free on HSC Math Hub.",
    pageCount: 117,
    isAvailable: true,
  },
  {
    id: "hsc-math-extension-2-book",
    title: "HSC MX2 Full",
    slug: "hsc-math-extension-2-book",
    pdfUrl: `${GITHUB_RAW_URL}/HSC-Math-Extension-2-Book/releases/HSC-Math-Extension-2-Book.pdf`,
    thumbnailPath: "/thumbnails/hsc-math-extension-2-book.png",
    cardBlurb: "The complete Extension 2 reference — arriving soon.",
    description:
      "HSC Mathematics Extension 2 full booklet — comprehensive coverage coming soon to HSC Math Hub. Browse other free HSC Maths booklets now.",
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
  // Web pages are 0-based: 0 = matte (PDF page 1).
  // booklet.pageCount is the total PDF page count.
  return Number.isSafeInteger(page) && page >= 0 && page < booklet.pageCount;
}
