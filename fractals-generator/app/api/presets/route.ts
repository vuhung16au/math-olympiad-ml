import { NextResponse } from 'next/server';
import { getAppPresets } from '../../lib/server-presets';

export const runtime = 'nodejs';

export async function GET(): Promise<NextResponse> {
  return NextResponse.json({ presets: getAppPresets() });
}
