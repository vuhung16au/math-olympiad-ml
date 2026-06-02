import { notFound } from "next/navigation";
import PDFViewer from "@/components/pages/PDFViewer";
import { getAvailableBooklets, getBookletBySlug } from "@/lib/booklets";
import {
  bookletOgImageUrl,
  buildBookletPageMetadata,
  buildNotFoundMetadata,
  clampOgDescription,
  SITE_URL,
} from "@/lib/og-metadata";

type BookletPageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return getAvailableBooklets().map((booklet) => ({ slug: booklet.slug }));
}

export async function generateMetadata({ params }: BookletPageProps) {
  const { slug } = await params;
  const booklet = getBookletBySlug(slug);
  const canonicalUrl = `${SITE_URL}/booklets/${slug}`;

  if (!booklet) {
    return buildNotFoundMetadata(canonicalUrl);
  }

  const title = `${booklet.title} — Page 0`;
  const description = clampOgDescription(
    booklet.description || `View Page 0 of ${booklet.title} on HSC Math Hub.`,
  );

  return buildBookletPageMetadata({
    title,
    description,
    canonicalUrl,
    imageUrl: bookletOgImageUrl(booklet.slug, 0),
  });
}

export default async function BookletPage({ params }: BookletPageProps) {
  const { slug } = await params;
  const booklet = getBookletBySlug(slug);

  if (!booklet || !booklet.isAvailable) {
    notFound();
  }

  return <PDFViewer booklet={booklet} initialPage={0} />;
}
