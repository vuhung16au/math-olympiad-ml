import sharp from "sharp";
import { getBookletBySlug, isValidBookletPage } from "@/lib/booklets";

export const runtime = "nodejs";

const SITE_URL = "https://hsc-math-hub.vercel.app";
const CACHE_CONTROL = "public, s-maxage=604800, stale-while-revalidate=2592000";
const IS_E2E_PDF_MOCK_ENABLED = process.env.NEXT_PUBLIC_E2E_MOCK_PDF === "1";

function parsePageParam(pageParam: string): number | null {
  const normalized = pageParam.endsWith(".png") ? pageParam.slice(0, -4) : pageParam;

  if (!/^\d+$/.test(normalized)) {
    return null;
  }

  const page = Number(normalized);
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
  const svg = `
    <svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
      <rect width="1200" height="630" fill="#ffffff"/>
      <rect x="48" y="48" width="1104" height="534" fill="#f3f4f6" stroke="#111827" stroke-width="2"/>
      <text x="600" y="300" font-size="34" text-anchor="middle" fill="#111827" font-family="Arial, Helvetica, sans-serif">
        Preview image unavailable
      </text>
    </svg>
  `;

  return sharp(Buffer.from(svg)).png().toBuffer();
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

async function renderPdfPageWithPdfjsCanvas(pdfArrayBuffer: ArrayBuffer, pageNumber: number): Promise<Buffer> {
  const pdfjs = await import("pdfjs-dist/legacy/build/pdf.mjs");
  const { createCanvas } = await import("@napi-rs/canvas");

  // Ensure the worker module is included in Vercel file-tracing.
  // pdf.js uses dynamic import for its worker, which can be missed by tracing unless referenced.
  await import("pdfjs-dist/legacy/build/pdf.worker.mjs");
  pdfjs.GlobalWorkerOptions.workerSrc = "pdfjs-dist/legacy/build/pdf.worker.mjs";

  const loadingTask = pdfjs.getDocument({ data: pdfArrayBuffer } as any);
  const doc = await loadingTask.promise;
  const pdfPage = await doc.getPage(pageNumber);

  // Render at a higher scale for crisp output, then resize.
  const viewport = pdfPage.getViewport({ scale: 2.0 });
  const canvas = createCanvas(Math.ceil(viewport.width), Math.ceil(viewport.height));
  const canvasContext = canvas.getContext("2d") as unknown as CanvasRenderingContext2D;

  await pdfPage.render({ canvasContext, viewport }).promise;

  return canvas.toBuffer("image/png");
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
  let errorStage: string | null = null;
  let pdfjsError: string | null = null;
  let sharpError: string | null = null;

  if (!booklet || !page || !isValidBookletPage(booklet, page)) {
    const fallback = await renderFallbackPng();
    return pngResponse(fallback, {
      status: 200,
      headers: {
        "Cache-Control": CACHE_CONTROL,
        "X-OG-Renderer": "fallback_invalid_params",
      },
    });
  }

  if (IS_E2E_PDF_MOCK_ENABLED) {
    const png = await renderE2EMockPng(booklet.slug, page);
    return pngResponse(png, {
      status: 200,
      headers: {
        "Cache-Control": CACHE_CONTROL,
        "X-OG-Renderer": "e2e_mock",
      },
    });
  }

  try {
    const pdfArrayBuffer = await fetchArrayBufferWithRetry(booklet.pdfUrl, 3);

    let pagePng: Buffer | null = null;
    let renderer: string | null = null;

    // Preferred: pdf.js -> canvas -> PNG (more reliable across environments).
    try {
      pagePng = await renderPdfPageWithPdfjsCanvas(pdfArrayBuffer, page);
      renderer = "pdfjs_canvas";
    } catch (err) {
      pdfjsError = err instanceof Error ? err.message : "unknown";
      errorStage = `pdfjs_canvas:${pdfjsError}`;
      pagePng = null;
    }

    // Fallback: attempt PDF rasterization via sharp/libvips.
    if (!pagePng) {
      try {
        const pdfBuffer = Buffer.from(pdfArrayBuffer);
        pagePng = await sharp(pdfBuffer, { density: 200, page: page - 1 })
          .png()
          .toBuffer();
        renderer = "sharp_pdf";
      } catch (err) {
        sharpError = err instanceof Error ? err.message : "unknown";
        // Keep the pdfjs error as the primary stage signal if present.
        if (!pdfjsError) {
          errorStage = `sharp_pdf:${sharpError}`;
        }
        throw err;
      }
    }

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
        "X-OG-Renderer": renderer ?? "unknown",
        ...(errorStage
          ? {
            "X-OG-Error-Stage": errorStage.slice(0, 180),
          }
          : null),
      },
    });
  } catch (err) {
    const errorText = err instanceof Error ? err.message : "unknown";
    const fallback = await renderFallbackPng();
    const headers: Record<string, string> = {
      // Don't cache transient failures as "blank previews".
      "Cache-Control": "no-store",
      "X-OG-Renderer": "fallback_error",
      "X-OG-Error": errorText.slice(0, 180),
    };

    if (errorStage) {
      headers["X-OG-Error-Stage"] = errorStage.slice(0, 180);
    }
    if (pdfjsError) {
      headers["X-OG-Error-Pdfjs"] = String(pdfjsError).slice(0, 180);
    }
    if (sharpError) {
      headers["X-OG-Error-Sharp"] = String(sharpError).slice(0, 180);
    }

    return pngResponse(fallback, {
      status: 200,
      headers: {
        ...headers,
      },
    });
  }
}

