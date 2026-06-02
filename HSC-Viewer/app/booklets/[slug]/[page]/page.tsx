import { notFound } from "next/navigation";
import PDFViewer from "@/components/pages/PDFViewer";
import { getBookletBySlug, isValidBookletPage } from "@/lib/booklets";
import {
  bookletOgImageUrl,
  bookletPageCanonicalUrl,
  buildBookletPageMetadata,
  buildNotFoundMetadata,
  clampOgDescription,
  OG_SHARE_QUERY_KEY,
} from "@/lib/og-metadata";

type BookletPageWithPageProps = {
  params: Promise<{ slug: string; page: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

function parsePageParam(pageParam: string): number | null {
  if (!/^\d+$/.test(pageParam)) {
    return null;
  }

  const page = Number(pageParam);
  if (!Number.isSafeInteger(page) || page < 0) {
    return null;
  }

  return page;
}

function readShareQueryVersion(
  searchParams: Record<string, string | string[] | undefined>,
): string | undefined {
  const raw = searchParams[OG_SHARE_QUERY_KEY];
  if (typeof raw === "string") {
    return raw;
  }
  if (Array.isArray(raw) && typeof raw[0] === "string") {
    return raw[0];
  }
  return undefined;
}

export async function generateMetadata({ params, searchParams }: BookletPageWithPageProps) {
  const { slug, page: pageParam } = await params;
  const resolvedSearchParams = await searchParams;
  const booklet = getBookletBySlug(slug);
  const page = parsePageParam(pageParam);
  const shareVersion = readShareQueryVersion(resolvedSearchParams);
  const canonicalUrl =
    booklet && page
      ? bookletPageCanonicalUrl(booklet.slug, page, shareVersion)
      : bookletPageCanonicalUrl(slug, parsePageParam(pageParam) ?? 0, shareVersion);

  if (!booklet || page === null || !isValidBookletPage(booklet, page)) {
    return buildNotFoundMetadata(canonicalUrl);
  }

  const title = `${booklet.title} — Page ${page}`;
  const description = clampOgDescription(
    booklet.description || `View Page ${page} of ${booklet.title} on HSC Math Hub.`,
  );

  return buildBookletPageMetadata({
    title,
    description,
    canonicalUrl,
    imageUrl: bookletOgImageUrl(booklet.slug, page),
  });
}

export default async function BookletPageWithPage({ params }: BookletPageWithPageProps) {
  const { slug, page: pageParam } = await params;
  const booklet = getBookletBySlug(slug);
  const page = parsePageParam(pageParam);

  if (!booklet || !booklet.isAvailable || page === null || !isValidBookletPage(booklet, page)) {
    notFound();
  }

  return <PDFViewer booklet={booklet} initialPage={page} />;
}
