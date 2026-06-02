import sharp from "sharp";
import { getBookletBySlug, isValidBookletPage } from "@/lib/booklets";
import { SITE_URL } from "@/lib/og-metadata";
import path from "path";

export const runtime = "nodejs";
/** Allow cold PDF render on first Facebook/Messenger scrape (Vercel default is 10s on hobby). */
export const maxDuration = 60;
const CACHE_CONTROL = "public, s-maxage=604800, stale-while-revalidate=2592000";
const IS_E2E_PDF_MOCK_ENABLED = process.env.NEXT_PUBLIC_E2E_MOCK_PDF === "1";

const OG_WIDTH = 1200;
const OG_HEIGHT = 630;
const LEFT_WIDTH = 640;
const RIGHT_WIDTH = OG_WIDTH - LEFT_WIDTH;

// Colors must come from styles/variables.css
const COLOR_PURPLE = "rgb(60, 16, 83)";
const COLOR_RED = "rgb(242, 18, 12)";
const COLOR_CHARCOAL = "rgb(48, 44, 42)";
const COLOR_IVORY = "rgb(242, 239, 235)";
const COLOR_WHITE = "rgb(255, 255, 255)";
const COLOR_STONE = "rgb(145, 139, 131)";

let didRegisterOgFont = false;

function parsePageParam(pageParam: string): number | null {
  const normalized = pageParam.endsWith(".png") ? pageParam.slice(0, -4) : pageParam;

  if (!/^\d+$/.test(normalized)) {
    return null;
  }

  const page = Number(normalized);
  // Web pages are 0-based: 0 = matte (PDF page 1).
  if (!Number.isSafeInteger(page) || page < 0) {
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

function clampText(text: string, maxChars: number): string {
  const trimmed = text.trim().replace(/\s+/g, " ");
  return trimmed.length > maxChars ? `${trimmed.slice(0, Math.max(0, maxChars - 1))}…` : trimmed;
}

function wrapText(text: string, maxCharsPerLine: number, maxLines: number): string[] {
  const words = text.trim().replace(/\s+/g, " ").split(" ").filter(Boolean);
  const lines: string[] = [];
  let current: string[] = [];

  for (const word of words) {
    const next = current.length === 0 ? word : `${current.join(" ")} ${word}`;
    if (next.length <= maxCharsPerLine) {
      current.push(word);
      continue;
    }
    if (current.length > 0) {
      lines.push(current.join(" "));
      current = [word];
    } else {
      lines.push(word.slice(0, maxCharsPerLine));
      current = [];
    }
    if (lines.length >= maxLines) break;
  }

  if (lines.length < maxLines && current.length > 0) {
    lines.push(current.join(" "));
  }

  if (lines.length > maxLines) {
    return lines.slice(0, maxLines);
  }

  // Add ellipsis if we truncated words.
  const consumedWords = lines.join(" ").split(" ").filter(Boolean).length;
  if (consumedWords < words.length && lines.length > 0) {
    lines[lines.length - 1] = clampText(lines[lines.length - 1], maxCharsPerLine);
  }
  return lines;
}

async function renderRightPanelPng(opts: {
  bookletTitle: string;
  page: number;
  description: string;
}): Promise<Buffer> {
  const { createCanvas, GlobalFonts } = await import("@napi-rs/canvas");

  if (!didRegisterOgFont) {
    // Ensure text renders reliably in serverless environments (no system fonts).
    GlobalFonts.registerFromPath(
      path.join(process.cwd(), "public", "og-fonts", "InterVariable.ttf"),
      "Inter",
    );
    didRegisterOgFont = true;
  }

  const title = opts.bookletTitle;
  const subtitle = `Page ${opts.page}`;
  const descLines = wrapText(opts.description, 34, 5);
  const siteHost = new URL(SITE_URL).host;

  const canvas = createCanvas(RIGHT_WIDTH, OG_HEIGHT);
  const ctx = canvas.getContext("2d");

  // Background + stripe
  ctx.fillStyle = COLOR_IVORY;
  ctx.fillRect(0, 0, RIGHT_WIDTH, OG_HEIGHT);
  ctx.fillStyle = COLOR_PURPLE;
  ctx.fillRect(0, 0, 10, OG_HEIGHT);

  // Brand
  ctx.fillStyle = COLOR_RED;
  ctx.font = "700 14px Inter, sans-serif";
  // letter spacing approximation by manual drawing
  const brand = "HSC MATH HUB";
  let x = 48;
  const yBrand = 92;
  for (const ch of brand) {
    ctx.fillText(ch, x, yBrand);
    x += ctx.measureText(ch).width + 1.6;
  }

  // Title
  ctx.fillStyle = COLOR_PURPLE;
  ctx.font = "800 40px Inter, sans-serif";
  ctx.fillText(clampText(title, 22), 48, 146);

  // Subtitle
  ctx.fillStyle = COLOR_CHARCOAL;
  ctx.font = "700 22px Inter, sans-serif";
  ctx.fillText(subtitle, 48, 194);

  // Divider
  ctx.strokeStyle = COLOR_STONE;
  ctx.globalAlpha = 0.55;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(48, 228);
  ctx.lineTo(RIGHT_WIDTH - 48, 228);
  ctx.stroke();
  ctx.globalAlpha = 1;

  // Description (wrapped)
  ctx.fillStyle = COLOR_CHARCOAL;
  ctx.font = "500 22px Inter, sans-serif";
  let y = 274;
  for (const line of descLines) {
    ctx.fillText(line, 48, y);
    y += 30;
  }

  // Footer
  ctx.fillStyle = COLOR_STONE;
  ctx.font = "400 14px Inter, sans-serif";
  ctx.fillText(siteHost, 48, OG_HEIGHT - 46);

  return canvas.toBuffer("image/png");
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
  const webPage = parsePageParam(pageParam);
  let errorStage: string | null = null;
  let pdfjsError: string | null = null;
  let sharpError: string | null = null;

  if (!booklet || webPage === null || !isValidBookletPage(booklet, webPage)) {
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
    const png = await renderE2EMockPng(booklet.slug, webPage);
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
    const pdfPageNumber = webPage + 1; // pdf.js pages are 1-based

    let pagePng: Buffer | null = null;
    let renderer: string | null = null;

    // Preferred: pdf.js -> canvas -> PNG (more reliable across environments).
    try {
      pagePng = await renderPdfPageWithPdfjsCanvas(pdfArrayBuffer, pdfPageNumber);
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
        // sharp's PDF page index is 0-based; webPage matches that.
        pagePng = await sharp(pdfBuffer, { density: 200, page: webPage })
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

    const leftPagePng = await sharp(pagePng)
      // Left side page raster (letterboxed)
      .resize(LEFT_WIDTH - 64, OG_HEIGHT - 96, { fit: "contain", background: COLOR_WHITE })
      .png()
      .toBuffer();

    // Compose the full 1200×630 image: left = page raster, right = text panel.
    const rightPng = await renderRightPanelPng({
      bookletTitle: booklet.title,
      page: webPage,
      description: booklet.description || `View Page ${webPage} of ${booklet.title} on HSC Math Hub.`,
    });

    const composedPng = await sharp({
      create: {
        width: OG_WIDTH,
        height: OG_HEIGHT,
        channels: 3,
        background: COLOR_WHITE,
      },
    })
      .composite([
        // Left background
        {
          input: await sharp({
            create: {
              width: LEFT_WIDTH,
              height: OG_HEIGHT,
              channels: 3,
              background: COLOR_WHITE,
            },
          })
            .png()
            .toBuffer(),
          left: 0,
          top: 0,
        },
        // Page image (centered in left pane)
        {
          input: leftPagePng,
          left: Math.floor((LEFT_WIDTH - (LEFT_WIDTH - 64)) / 2),
          top: Math.floor((OG_HEIGHT - (OG_HEIGHT - 96)) / 2),
        },
        // Subtle border around the page area
        {
          input: Buffer.from(
            `<svg width="${LEFT_WIDTH}" height="${OG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
              <rect x="32" y="48" width="${LEFT_WIDTH - 64}" height="${OG_HEIGHT - 96}" fill="none" stroke="${COLOR_STONE}" stroke-width="2" opacity="0.55"/>
            </svg>`,
          ),
          left: 0,
          top: 0,
        },
        // Right panel
        {
          input: rightPng,
          left: LEFT_WIDTH,
          top: 0,
        },
      ])
      .png()
      .toBuffer();

    return pngResponse(composedPng, {
      status: 200,
      headers: {
        "Cache-Control": CACHE_CONTROL,
        // Helpful for debugging which page was requested.
        "X-OG-Booklet": booklet.slug,
        "X-OG-Page": String(webPage),
        "X-OG-Pdf-Page": String(pdfPageNumber),
        "X-OG-Source": `${SITE_URL}/booklets/${booklet.slug}/${webPage}`,
        "X-OG-Renderer": `${renderer ?? "unknown"}_composed`,
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

