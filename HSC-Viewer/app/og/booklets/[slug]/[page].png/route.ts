import { NextResponse } from "next/server";
import sharp from "sharp";
import { getBookletBySlug, isValidBookletPage } from "@/lib/booklets";

export const runtime = "nodejs";

const SITE_URL = "https://hsc-math-hub.vercel.app";
const CACHE_CONTROL = "public, s-maxage=604800, stale-while-revalidate=2592000";
const IS_E2E_PDF_MOCK_ENABLED = process.env.NEXT_PUBLIC_E2E_MOCK_PDF === "1";

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

async function fetchArrayBufferWithRetry(url: string, retries = 3): Promise<ArrayBuffer> {
  let lastErr: unknown = null;

  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      return await res.arrayBuffer();
    } catch (err) {
      lastErr = err;
      await new Promise((r) => setTimeout(r, 250 * (i + 1)));
    }
  }

  throw lastErr instanceof Error ? lastErr : new Error("Failed to fetch PDF");
}

async function renderFallbackPng(): Promise<Buffer> {
  // A deterministic, simple PNG so crawlers never see a broken image.
  return sharp({
    create: {
      width: 1200,
      height: 630,
      channels: 3,
      background: "#ffffff",
    },
  })
    .png()
    .toBuffer();
}

async function renderE2EMockPng(slug: string, page: number): Promise<Buffer> {
  const svg = `
    <svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
      <rect width="1200" height="630" fill="#ffffff"/>
      <rect x="40" y="40" width="1120" height="550" fill="#f3f4f6" stroke="#111827" stroke-width="2"/>
      <text x="600" y="290" font-size="44" text-anchor="middle" fill="#111827" font-family="Arial, Helvetica, sans-serif">
        OG Image (E2E Mock)
      </text>
      <text x="600" y="360" font-size="28" text-anchor="middle" fill="#111827" font-family="Arial, Helvetica, sans-serif">
        ${slug} — Page ${page}
      </text>
    </svg>
  `;

  return sharp(Buffer.from(svg))
    .png()
    .toBuffer();
}

function pngResponse(png: Buffer, init?: ResponseInit): Response {
  return new Response(new Uint8Array(png), {
    ...init,
    headers: {
      "Content-Type": "image/png",
      ...init?.headers,
    },
  });
}

export async function GET(
  _request: Request,
  context: { params: Promise<{ slug: string; page: string }> }
) {
  const { slug, page: pageParam } = await context.params;
  const booklet = getBookletBySlug(slug);
  const page = parsePageParam(pageParam);

  if (!booklet || !page || !isValidBookletPage(booklet, page)) {
    const fallback = await renderFallbackPng();
    return pngResponse(fallback, {
      status: 200,
      headers: {
        "Cache-Control": CACHE_CONTROL,
      },
    });
  }

  if (IS_E2E_PDF_MOCK_ENABLED) {
    const png = await renderE2EMockPng(booklet.slug, page);
    return pngResponse(png, {
      status: 200,
      headers: {
        "Cache-Control": CACHE_CONTROL,
      },
    });
  }

  try {
    const pdfArrayBuffer = await fetchArrayBufferWithRetry(booklet.pdfUrl, 3);

    // Render the requested PDF page directly via sharp/libvips.
    // This avoids native canvas bindings and works well with Vercel's sharp builds.
    const pdfBuffer = Buffer.from(pdfArrayBuffer);
    const pagePng = await sharp(pdfBuffer, { density: 200, page: page - 1 })
      .png()
      .toBuffer();

    const finalPng = await sharp(pagePng)
      .resize(1200, 630, { fit: "contain", background: "#ffffff" })
      .png()
      .toBuffer();

    return pngResponse(finalPng, {
      status: 200,
      headers: {
        "Cache-Control": CACHE_CONTROL,
        // Helpful for debugging which page was requested.
        "X-OG-Booklet": booklet.slug,
        "X-OG-Page": String(page),
        "X-OG-Source": `${SITE_URL}/booklets/${booklet.slug}/${page}`,
      },
    });
  } catch {
    const fallback = await renderFallbackPng();
    return pngResponse(fallback, {
      status: 200,
      headers: {
        "Cache-Control": CACHE_CONTROL,
      },
    });
  }
}

