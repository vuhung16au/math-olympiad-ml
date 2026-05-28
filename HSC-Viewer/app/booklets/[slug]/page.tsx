import type { Metadata } from "next";
import { notFound } from "next/navigation";
import PDFViewer from "@/components/pages/PDFViewer";
import { getAvailableBooklets, getBookletBySlug } from "@/lib/booklets";

type BookletPageProps = {
  params: Promise<{ slug: string }>;
};

const SITE_URL = "https://hsc-math-hub.vercel.app";

function clampDescription(description: string): string {
  const trimmed = description.trim();
  return trimmed.length > 200 ? `${trimmed.slice(0, 197)}...` : trimmed;
}

function getNotFoundMetadata(url: string): Metadata {
  const title = "Page not found — HSC Math Hub";
  const description = "This page does not exist. Browse booklets on HSC Math Hub.";

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      url,
      type: "website",
      siteName: "HSC Math Hub",
      images: [
        {
          url: `${SITE_URL}/og/site-fallback.png`,
          width: 1200,
          height: 630,
        },
      ],
    },
  };
}

export function generateStaticParams() {
  return getAvailableBooklets().map((booklet) => ({ slug: booklet.slug }));
}

export async function generateMetadata({ params }: BookletPageProps): Promise<Metadata> {
  const { slug } = await params;
  const booklet = getBookletBySlug(slug);
  const url = `${SITE_URL}/booklets/${slug}`;

  if (!booklet) {
    return getNotFoundMetadata(url);
  }

  const title = `${booklet.title} — Page 1`;
  const description = clampDescription(booklet.description || `View Page 1 of ${booklet.title} on HSC Math Hub.`);
  const imageUrl = `${SITE_URL}/og/booklets/${booklet.slug}/1.png`;

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      url,
      type: "website",
      siteName: "HSC Math Hub",
      images: [{ url: imageUrl, width: 1200, height: 630 }],
    },
  };
}

export default async function BookletPage({ params }: BookletPageProps) {
  const { slug } = await params;
  const booklet = getBookletBySlug(slug);

  if (!booklet || !booklet.isAvailable) {
    notFound();
  }

  return <PDFViewer booklet={booklet} initialPage={1} />;
}
