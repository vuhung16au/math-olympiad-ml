import { promises as fs } from "node:fs";
import path from "node:path";
import { GENERATED_MANIFEST } from "@/lib/constants";
import type { BookletManifestEntry, GeneratedBookletDocument } from "@/lib/booklets";

const projectRoot = /* turbopackIgnore: true */ process.cwd();

function getVisibleBookletFilter() {
  const raw = process.env.VISIBLE_BOOKLETS?.trim();
  if (!raw) {
    return null;
  }

  const slugs = raw
    .split(",")
    .map((entry) => entry.trim().toLowerCase())
    .filter((entry) => entry.length > 0);

  return slugs.length > 0 ? new Set(slugs) : null;
}

async function readJsonFile<T>(filePath: string): Promise<T | null> {
  try {
    const content = await fs.readFile(path.join(projectRoot, filePath), "utf8");
    return JSON.parse(content) as T;
  } catch {
    return null;
  }
}

export async function getGeneratedManifest(): Promise<BookletManifestEntry[]> {
  const manifest = (await readJsonFile<BookletManifestEntry[]>(GENERATED_MANIFEST)) ?? [];
  const visibleFilter = getVisibleBookletFilter();

  if (!visibleFilter) {
    return manifest;
  }

  return manifest.filter((entry) => visibleFilter.has(entry.slug.toLowerCase()));
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
