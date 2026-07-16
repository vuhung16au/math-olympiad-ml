#!/usr/bin/env npx tsx
/**
 * Render 5 escape-time fractals to PNG using the server-side renderer.
 * Called by generate-5-fractals-for-booklets.js.
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { PNG } from 'pngjs';
import { renderFractalImage } from '../app/lib/server-render-algos';
import { getAppPresets } from '../app/lib/server-presets';
import { parseColor } from '../app/lib/server-render-utils';

const OUT_DIR = process.argv[2];
if (!OUT_DIR) {
  console.error('Usage: npx tsx scripts/render-5-fractals-png.ts <out-dir>');
  process.exit(1);
}

const A4_PORTRAIT_W = 595;
const A4_PORTRAIT_H = 842;

const TARGETS = [
  // -- original 5 --
  { family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-classic',
    scheme: 'acu', params: { etMaxIterations: '300' } },
  { family: 'escapeTime', preset: 'burningShip', slug: 'burning-ship',
    scheme: 'acu', params: { etMaxIterations: '400' } },
  { family: 'escapeTime', preset: 'multibrot', slug: 'multibrot',
    scheme: 'matrix', params: { etMaxIterations: '420', etPower: '3' } },
  { family: 'escapeTime', preset: 'juliaClassic', slug: 'julia-classic',
    scheme: 'acu', params: { etMaxIterations: '350' } },
  { family: 'escapeTime', preset: 'mandelbrotDoubleHook', slug: 'mandelbrot-double-hook',
    scheme: 'acu', params: { etMaxIterations: '600' } },

  // -- 10 new variants --
  { family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-matrix',
    scheme: 'matrix', params: { etMaxIterations: '400' } },
  { family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-power4',
    scheme: 'acu', params: { etMaxIterations: '300', etPower: '4' } },
  { family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-hiiter',
    scheme: 'acu', params: { etMaxIterations: '800' } },
  { family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-loiter',
    scheme: 'acu', params: { etMaxIterations: '150' } },
  { family: 'escapeTime', preset: 'burningShip', slug: 'burning-ship-matrix',
    scheme: 'matrix', params: { etMaxIterations: '400' } },
  { family: 'escapeTime', preset: 'juliaClassic', slug: 'julia-dendrite',
    scheme: 'acu', params: { etMaxIterations: '350', etJuliaRe: '-0.4', etJuliaIm: '0.6' } },
  { family: 'escapeTime', preset: 'juliaProbability', slug: 'julia-spiral',
    scheme: 'acu', params: { etMaxIterations: '450', etJuliaRe: '-0.7269', etJuliaIm: '0.1889' } },
  { family: 'escapeTime', preset: 'juliaClassic', slug: 'julia-power3',
    scheme: 'acu', params: { etMaxIterations: '300', etPower: '3' } },
  { family: 'escapeTime', preset: 'juliaVectors', slug: 'julia-matrix',
    scheme: 'matrix', params: { etMaxIterations: '350', etJuliaRe: '0.285', etJuliaIm: '0.01' } },
  { family: 'escapeTime', preset: 'juliaSequences', slug: 'julia-feather',
    scheme: 'acu', params: { etMaxIterations: '400', etJuliaRe: '-0.1', etJuliaIm: '0.8' } },
];

async function main() {
  const presets = getAppPresets();
  const bg = parseColor('#ffffff', [255, 255, 255]);

  for (let i = 0; i < TARGETS.length; i += 1) {
    const row = TARGETS[i];
    const preset = presets[row.family]?.[row.preset];
    if (!preset) {
      console.warn(`Skip missing preset: ${row.family}/${row.preset}`);
      continue;
    }

    const image = renderFractalImage(
      row.family as any,
      A4_PORTRAIT_W,
      A4_PORTRAIT_H,
      preset,
      row.params,
      row.scheme,
      bg,
    );

    const png = new PNG({ width: A4_PORTRAIT_W, height: A4_PORTRAIT_H });
    png.data = Buffer.from(image);
    const n = String(i + 1).padStart(2, '0');
    const pngPath = path.join(OUT_DIR, `${n}-${row.slug}.png`);
    await fs.writeFile(pngPath, PNG.sync.write(png));
    console.log(`Wrote ${pngPath}`);
  }
  console.log('Done.');
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});
