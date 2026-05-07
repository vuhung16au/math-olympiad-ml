import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getVisibleBooklets } from "@/lib/booklets";
import { getGeneratedBookletBySlug, getGeneratedManifest } from "@/lib/generated-content";
import ReaderShell from "@/components/reader/ReaderShell";

type BookletPageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateStaticParams() {
  const manifest = getVisibleBooklets(await getGeneratedManifest());
  return manifest.map((booklet) => ({ slug: booklet.slug }));
}

export async function generateMetadata({
  params,
}: BookletPageProps): Promise<Metadata> {
  const { slug } = await params;
  const booklet = await getGeneratedBookletBySlug(slug);

  if (!booklet) {
    return {};
  }

  return {
    title: `${booklet.title} | HSC Viewer MathJax`,
    description: `Read ${booklet.title} online.`,
  };
}

export default async function BookletPage({ params }: BookletPageProps) {
  const { slug } = await params;
  const booklet = await getGeneratedBookletBySlug(slug);

  if (!booklet) {
    notFound();
  }

  return <ReaderShell booklet={booklet} />;
}
