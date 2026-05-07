import { promises as fs } from "node:fs";
import path from "node:path";

const MIME_TYPES: Record<string, string> = {
  ".css": "text/css; charset=utf-8",
  ".gif": "image/gif",
  ".html": "text/html; charset=utf-8",
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".json": "application/json; charset=utf-8",
  ".mml": "application/mathml+xml",
  ".pdf": "application/pdf",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".webp": "image/webp",
};

type RouteProps = {
  params: Promise<{ slug: string; assetPath: string[] }>;
};

export async function GET(_request: Request, { params }: RouteProps) {
  const { slug, assetPath } = await params;
  const filePath = path.join(process.cwd(), ".generated", "assets", slug, ...assetPath);

  try {
    const data = await fs.readFile(filePath);
    const ext = path.extname(filePath).toLowerCase();

    return new Response(data, {
      headers: {
        "content-type": MIME_TYPES[ext] ?? "application/octet-stream",
        "cache-control": "public, max-age=3600",
      },
    });
  } catch {
    return new Response("Not found", { status: 404 });
  }
}
