import type { Metadata } from "next";

/**
 * Bump when OG image layout or generator changes (forces Facebook/Messenger re-fetch).
 * Path-based image URLs (`/og/preview-{version}/...`) — no query string on og:image.
 */
export const OG_IMAGE_VERSION = "6";

/** Query param for share URLs to bust Meta link-preview cache per version. */
export const OG_SHARE_QUERY_KEY = "m";

/** Production site URL. Set `NEXT_PUBLIC_SITE_URL` when using a custom domain. */
export const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL?.replace(/\/$/, "") ??
  "https://hsc-math-hub.vercel.app";

export const SITE_NAME = "HSC Math Hub";

const FB_APP_ID = process.env.NEXT_PUBLIC_FB_APP_ID ?? process.env.FB_APP_ID;

/**
 * How og:image is chosen:
 * - `dynamic` (default): per-page PNG from `/og/preview-{version}/...` (Discord, FB Pages).
 * - `static`: booklet cover from `/thumbnails/{slug}.png` on this site (fast, no serverless).
 * - `github`: same cover on raw.githubusercontent.com (tests Messenger vs vercel.app).
 */
export type OgImageMode = "dynamic" | "static" | "github";

const GITHUB_OG_BASE =
  "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Viewer/public";

export function getOgImageMode(): OgImageMode {
  const mode = process.env.NEXT_PUBLIC_OG_IMAGE_MODE;
  if (mode === "static" || mode === "github" || mode === "dynamic") {
    return mode;
  }
  return "dynamic";
}

export function clampOgDescription(description: string): string {
  const trimmed = description.trim();
  return trimmed.length > 200 ? `${trimmed.slice(0, 197)}...` : trimmed;
}

/** Absolute og:image URL for Meta crawlers. */
export function bookletOgImageUrl(slug: string, page: number): string {
  const mode = getOgImageMode();

  if (mode === "github") {
    return `${GITHUB_OG_BASE}/thumbnails/${slug}.png`;
  }

  if (mode === "static") {
    return `${SITE_URL}/thumbnails/${slug}.png`;
  }

  return `${SITE_URL}/og/preview-${OG_IMAGE_VERSION}/booklets/${slug}/${page}.png`;
}

/** URL to paste in chats; `?m=` creates a fresh link-preview cache key at Meta. */
export function bookletPageShareUrl(slug: string, page: number): string {
  return `${SITE_URL}/booklets/${slug}/${page}?${OG_SHARE_QUERY_KEY}=${OG_IMAGE_VERSION}`;
}

export function bookletPageCanonicalUrl(slug: string, page: number, shareQuery?: string): string {
  if (shareQuery === OG_IMAGE_VERSION) {
    return bookletPageShareUrl(slug, page);
  }
  return `${SITE_URL}/booklets/${slug}/${page}`;
}

function buildOgImage(imageUrl: string, alt: string) {
  return {
    url: imageUrl,
    secureUrl: imageUrl,
    width: 1200,
    height: 630,
    type: "image/png" as const,
    alt,
  };
}

export function buildBookletPageMetadata(input: {
  title: string;
  description: string;
  canonicalUrl: string;
  imageUrl: string;
  keywords?: string[];
}): Metadata {
  const description = clampOgDescription(input.description);

  const metadata: Metadata = {
    metadataBase: new URL(SITE_URL),
    title: input.title,
    description,
    keywords: input.keywords,
    alternates: {
      canonical: input.canonicalUrl,
    },
    openGraph: {
      title: input.title,
      description,
      url: input.canonicalUrl,
      type: "website",
      siteName: SITE_NAME,
      locale: "en_AU",
      images: [buildOgImage(input.imageUrl, input.title)],
    },
    twitter: {
      card: "summary_large_image",
      title: input.title,
      description,
      images: [buildOgImage(input.imageUrl, input.title)],
    },
  };

  if (FB_APP_ID) {
    metadata.other = {
      "fb:app_id": FB_APP_ID,
    };
  }

  return metadata;
}

export function buildNotFoundMetadata(canonicalUrl: string): Metadata {
  const title = "Page not found — HSC Math Hub";
  const description = "This page does not exist. Browse booklets on HSC Math Hub.";
  const imageUrl = `${SITE_URL}/og/site-fallback.png`;

  return buildBookletPageMetadata({
    title,
    description,
    canonicalUrl,
    imageUrl,
  });
}
