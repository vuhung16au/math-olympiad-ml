import type { Metadata } from "next";
import { notFound } from "next/navigation";
import PDFViewer from "@/components/pages/PDFViewer";
import { getBookletBySlug } from "@/lib/booklets";

type BookletPageWithPageProps = {
  params: Promise<{ slug: string; page: string }>;
};

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

  if (!booklet || !page) {
    return {};
  }

  return {
    title: `${booklet.title} - Page ${page} | HSC Math Hub`,
    description: `Open ${booklet.title} directly in the browser at page ${page}.`,
  };
}

export default async function BookletPageWithPage({ params }: BookletPageWithPageProps) {
  const { slug, page: pageParam } = await params;
  const booklet = getBookletBySlug(slug);
  const page = parsePageParam(pageParam);

  if (!booklet || !booklet.isAvailable || !page) {
    notFound();
  }

  return <PDFViewer booklet={booklet} initialPage={page} />;
}
