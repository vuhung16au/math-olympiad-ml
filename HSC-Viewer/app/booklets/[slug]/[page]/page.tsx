import type { Metadata } from "next";
import { notFound } from "next/navigation";
import PDFViewer from "@/components/pages/PDFViewer";
import { getBookletBySlug, isValidBookletPage } from "@/lib/booklets";

type BookletPageWithPageProps = {
  params: Promise<{ slug: string; page: string }>;
};

const SITE_URL = "https://hsc-math-hub.vercel.app";
const OG_IMAGE_VERSION = "4";

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

function parsePageParam(pageParam: string): number | null {
  if (!/^\d+$/.test(pageParam)) {
    return null;
  }

  const page = Number(pageParam);
  if (!Number.isSafeInteger(page) || page < 1) {
    return null;
  }

  return page;
}

export async function generateMetadata({ params }: BookletPageWithPageProps): Promise<Metadata> {
  const { slug, page: pageParam } = await params;
  const booklet = getBookletBySlug(slug);
  const page = parsePageParam(pageParam);
  const url = `${SITE_URL}/booklets/${slug}/${pageParam}`;

  if (!booklet || !page || !isValidBookletPage(booklet, page)) {
    return getNotFoundMetadata(url);
  }

  const title = `${booklet.title} — Page ${page}`;
  const description = clampDescription(booklet.description || `View Page ${page} of ${booklet.title} on HSC Math Hub.`);
  const imageUrl = `${SITE_URL}/og/booklets/${booklet.slug}/${page}.png?v=${OG_IMAGE_VERSION}`;

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

export default async function BookletPageWithPage({ params }: BookletPageWithPageProps) {
  const { slug, page: pageParam } = await params;
  const booklet = getBookletBySlug(slug);
  const page = parsePageParam(pageParam);

  if (!booklet || !booklet.isAvailable || !page || !isValidBookletPage(booklet, page)) {
    notFound();
  }

  return <PDFViewer booklet={booklet} initialPage={page} />;
}
