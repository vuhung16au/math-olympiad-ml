import sharp from "sharp";

export const runtime = "nodejs";

const CACHE_CONTROL = "public, s-maxage=604800, stale-while-revalidate=2592000";

export async function GET() {
  const png = await sharp({
    create: {
      width: 1200,
      height: 630,
      channels: 3,
      background: "#ffffff",
    },
  })
    .png()
    .toBuffer();

  return new Response(new Uint8Array(png), {
    status: 200,
    headers: {
      "Content-Type": "image/png",
      "Cache-Control": CACHE_CONTROL,
    },
  });
}

