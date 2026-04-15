import { NextRequest, NextResponse } from 'next/server';
import { PNG } from 'pngjs';
import { parseColor, renderFractalImage, resolveFractalFamily } from '../../../../lib/server-render';
import { getAppPresets } from '../../../../lib/server-presets';

export const runtime = 'nodejs';

const DEFAULT_WIDTH = 1280;
const DEFAULT_HEIGHT = 720;
const MIN_SIZE = 32;
const MAX_SIZE = 4096;
const ALLOWED_SCHEMES = new Set(['acu', 'matrix', 'emerald', 'ink']);

function parseDimension(input: string | null, fallback: number): number {
  if (!input) return fallback;
  const parsed = Number.parseInt(input, 10);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function readValidatedSize(url: URL): { width: number; height: number; error?: string } {
  const width = parseDimension(url.searchParams.get('width'), DEFAULT_WIDTH);
  const height = parseDimension(url.searchParams.get('height'), DEFAULT_HEIGHT);
  if (width < MIN_SIZE || width > MAX_SIZE || height < MIN_SIZE || height > MAX_SIZE) {
    return { width, height, error: `width/height must be between ${MIN_SIZE} and ${MAX_SIZE}` };
  }
  return { width, height };
}

function normalizeMainColorScheme(url: URL): string {
  const value = (url.searchParams.get('mainColorScheme') ?? 'acu').trim().toLowerCase();
  return ALLOWED_SCHEMES.has(value) ? value : 'acu';
}

function readParams(url: URL): Record<string, string> {
  const params: Record<string, string> = {};
  for (const [key, value] of url.searchParams.entries()) {
    params[key] = value;
  }
  return params;
}

export async function GET(
  request: NextRequest,
  context: { params: Promise<{ family: string; preset: string }> },
): Promise<NextResponse> {
  const { family: familyRaw, preset: presetKey } = await context.params;
  const family = resolveFractalFamily(familyRaw);
  if (!family) {
    return NextResponse.json({ error: `Unknown family "${familyRaw}"` }, { status: 404 });
  }

  const size = readValidatedSize(request.nextUrl);
  if (size.error) {
    return NextResponse.json({ error: size.error }, { status: 400 });
  }

  const presets = getAppPresets();
  const preset = presets[family]?.[presetKey];
  if (!preset) {
    return NextResponse.json({ error: `Unknown preset ${familyRaw}/${presetKey}` }, { status: 404 });
  }

  const params = readParams(request.nextUrl);
  const mainColorScheme = normalizeMainColorScheme(request.nextUrl);
  const backgroundColor = parseColor(request.nextUrl.searchParams.get('backgroundColor'), [255, 255, 255]);

  const image = renderFractalImage(family, size.width, size.height, preset, params, mainColorScheme, backgroundColor);
  const png = new PNG({ width: size.width, height: size.height });
  png.data = Buffer.from(image);
  const output = PNG.sync.write(png);
  const body = new Uint8Array(output);

  return new NextResponse(body, {
    status: 200,
    headers: {
      'content-type': 'image/png',
      'cache-control': 'public, max-age=3600, s-maxage=86400',
      'content-disposition': `inline; filename="${familyRaw}-${presetKey}.png"`,
    },
  });
}
