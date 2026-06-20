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

  const title = `Page 0 - ${booklet.title} | HSC Math Hub`;
  const description = clampOgDescription(
    booklet.description || `View Page 0 of ${booklet.title} on HSC Math Hub.`,
  );

  return buildBookletPageMetadata({
    title,
    description,
    canonicalUrl,
    imageUrl: bookletOgImageUrl(booklet.slug, 0),
    keywords: booklet.keywords,
  });
}

export default async function BookletPage({ params }: BookletPageProps) {
  const { slug } = await params;
  const booklet = getBookletBySlug(slug);

  if (!booklet || !booklet.isAvailable) {
    notFound();
  }

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Course",
    "name": booklet.title,
    "description": booklet.description,
    "provider": {
      "@type": "Organization",
      "name": "HSC Math Hub",
      "sameAs": SITE_URL
    },
    "educationalLevel": "NSW HSC"
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <PDFViewer booklet={booklet} initialPage={0} />
    </>
  );
}
