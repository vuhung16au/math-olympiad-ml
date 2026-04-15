import { NextRequest, NextResponse } from 'next/server';
import { renderFractalImage } from '../../lib/server-render';
import { getAppPresets } from '../../lib/server-presets';

export const runtime = 'nodejs';

type RenderPayload = {
  family: string;
  preset: string;
  width: number;
  height: number;
  params: Record<string, unknown>;
};

function parsePayload(body: any): RenderPayload {
  return {
    family: String(body.family),
    preset: String(body.preset),
    width: Number(body.width ?? 980),
    height: Number(body.height ?? 760),
    params: body.params ?? {},
  };
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  const payload = parsePayload(await request.json());
  const family = payload.family as keyof ReturnType<typeof getAppPresets>;
  const presets = getAppPresets();
  const preset = presets[family]?.[payload.preset];
  if (!preset) {
    return NextResponse.json({ error: `Unknown preset ${family}/${payload.preset}` }, { status: 400 });
  }
  const image = renderFractalImage(family, payload.width, payload.height, preset, payload.params, 'acu', [255, 255, 255]);
  return NextResponse.json({ image: Array.from(image), meta: `Rendered ${family}/${payload.preset}` });
}
