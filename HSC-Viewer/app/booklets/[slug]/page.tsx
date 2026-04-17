import type { Metadata } from "next";
import { notFound } from "next/navigation";
import PDFViewer from "@/components/pages/PDFViewer";
import { getAvailableBooklets, getBookletBySlug } from "@/lib/booklets";

type BookletPageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return getAvailableBooklets().map((booklet) => ({ slug: booklet.slug }));
}

export async function generateMetadata({ params }: BookletPageProps): Promise<Metadata> {
  const { slug } = await params;
  const booklet = getBookletBySlug(slug);

  if (!booklet) {
    return {};
  }

  return {
    title: `${booklet.title} | HSC Math Hub`,
    description: `Open ${booklet.title} directly in the browser.`,
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
