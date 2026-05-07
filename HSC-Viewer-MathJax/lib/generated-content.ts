import { promises as fs } from "node:fs";
import path from "node:path";
import { GENERATED_MANIFEST } from "@/lib/constants";
import type { BookletManifestEntry, GeneratedBookletDocument } from "@/lib/booklets";

const projectRoot = /* turbopackIgnore: true */ process.cwd();

async function readJsonFile<T>(filePath: string): Promise<T | null> {
  try {
    const content = await fs.readFile(path.join(projectRoot, filePath), "utf8");
    return JSON.parse(content) as T;
  } catch {
    return null;
  }
}

export async function getGeneratedManifest(): Promise<BookletManifestEntry[]> {
  return (await readJsonFile<BookletManifestEntry[]>(GENERATED_MANIFEST)) ?? [];
}

export async function getGeneratedBookletBySlug(
  slug: string,
): Promise<GeneratedBookletDocument | null> {
  const manifest = await getGeneratedManifest();
  const booklet = manifest.find((entry) => entry.slug === slug);

  if (!booklet) {
    return null;
  }

  const html = await fs.readFile(path.join(projectRoot, booklet.htmlPath), "utf8");

  return {
    slug: booklet.slug,
    title: booklet.title,
    html,
    warningCount: booklet.conversionWarnings.length,
    conversionWarnings: booklet.conversionWarnings,
    assetBasePath: booklet.assetBasePath,
    lastGeneratedAt: booklet.lastGeneratedAt,
  };
}
