import type { FractalType } from '../types';

export type AnyRecord = Record<string, any>;
export type Rgb = [number, number, number];

export const ACU_GRADIENT: Rgb[] = [
  [9, 10, 38],
  [45, 78, 140],
  [98, 187, 255],
  [255, 236, 130],
  [255, 140, 66],
];

export const IFS_MATRIX_PALETTE: Rgb[] = [
  [16, 185, 129],
  [5, 150, 105],
  [34, 197, 94],
  [20, 184, 166],
  [6, 182, 212],
  [59, 130, 246],
];

const FAMILY_ALIASES: Record<string, FractalType> = {
  ifs: 'ifs',
  lsystem: 'lsystem',
  'l-system': 'lsystem',
  escape: 'escapeTime',
  'escape-time': 'escapeTime',
  escapetime: 'escapeTime',
  newton: 'newton',
  attractor: 'attractor',
  'strange-attractor': 'attractor',
  inversion: 'inversion',
  'circle-inversion': 'inversion',
};

export function resolveFractalFamily(familyInput: string): FractalType | null {
  return FAMILY_ALIASES[familyInput.toLowerCase()] ?? null;
}

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

export function gradientColor(t: number, scheme: string): Rgb {
  if (scheme === 'emerald') return [5, 150, 105];
  if (scheme === 'ink') return [17, 24, 39];
  if (scheme === 'matrix') {
    const idx = Math.max(0, Math.min(IFS_MATRIX_PALETTE.length - 1, Math.floor(t * IFS_MATRIX_PALETTE.length)));
    return IFS_MATRIX_PALETTE[idx];
  }
  const clamped = Math.max(0, Math.min(1, t));
  const scaled = clamped * (ACU_GRADIENT.length - 1);
  const i = Math.floor(scaled);
  const f = scaled - i;
  const c1 = ACU_GRADIENT[i];
  const c2 = ACU_GRADIENT[Math.min(ACU_GRADIENT.length - 1, i + 1)];
  return [
    Math.round(lerp(c1[0], c2[0], f)),
    Math.round(lerp(c1[1], c2[1], f)),
    Math.round(lerp(c1[2], c2[2], f)),
  ];
}

export function setPixel(image: Uint8ClampedArray, width: number, x: number, y: number, r: number, g: number, b: number): void {
  if (x < 0 || y < 0) return;
  const idx = (y * width + x) * 4;
  if (idx < 0 || idx + 3 >= image.length) return;
  image[idx] = r;
  image[idx + 1] = g;
  image[idx + 2] = b;
  image[idx + 3] = 255;
}

export function drawSquare(image: Uint8ClampedArray, width: number, x: number, y: number, size: number, color: Rgb): void {
  const radius = Math.max(0, Math.floor(size / 2));
  for (let dy = -radius; dy <= radius; dy += 1) {
    for (let dx = -radius; dx <= radius; dx += 1) {
      setPixel(image, width, x + dx, y + dy, color[0], color[1], color[2]);
    }
  }
}

export function drawLine(
  image: Uint8ClampedArray,
  width: number,
  x0: number,
  y0: number,
  x1: number,
  y1: number,
  color: Rgb,
  lineWidth = 1,
): void {
  const dx = Math.abs(x1 - x0);
  const sx = x0 < x1 ? 1 : -1;
  const dy = -Math.abs(y1 - y0);
  const sy = y0 < y1 ? 1 : -1;
  let err = dx + dy;
  let x = x0;
  let y = y0;
  while (true) {
    drawSquare(image, width, x, y, lineWidth, color);
    if (x === x1 && y === y1) break;
    const e2 = 2 * err;
    if (e2 >= dy) {
      err += dy;
      x += sx;
    }
    if (e2 <= dx) {
      err += dx;
      y += sy;
    }
  }
}

export function parseRules(text: string): Record<string, string> {
  return Object.fromEntries(
    text
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => {
        const idx = line.indexOf('=');
        return [line.slice(0, idx).trim(), line.slice(idx + 1).trim()];
      }),
  );
}

export function createTransform(bounds: [number, number, number, number], width: number, height: number, padding = 24): (x: number, y: number) => [number, number] {
  const [maxX, maxY, minX, minY] = bounds;
  const boundsW = Math.max(1, maxX - minX);
  const boundsH = Math.max(1, maxY - minY);
  const scale = Math.min((width - padding * 2) / boundsW, (height - padding * 2) / boundsH);
  const offsetX = (width - boundsW * scale) / 2;
  const offsetY = (height - boundsH * scale) / 2;
  return (x: number, y: number): [number, number] => [
    Math.round((x - minX) * scale + offsetX),
    Math.round(height - ((y - minY) * scale + offsetY)),
  ];
}

export function mapPixelToComplex(
  x: number,
  y: number,
  width: number,
  height: number,
  viewport: { minX: number; maxX: number; minY: number; maxY: number },
): [number, number] {
  const re = viewport.minX + (x / (width - 1)) * (viewport.maxX - viewport.minX);
  const im = viewport.maxY - (y / (height - 1)) * (viewport.maxY - viewport.minY);
  return [re, im];
}

export function parseColor(input: string | null | undefined, fallback: Rgb): Rgb {
  if (!input) return fallback;
  const lower = input.trim().toLowerCase();
  if (lower === 'white') return [255, 255, 255];
  if (lower === 'black') return [0, 0, 0];
  const hex = lower.startsWith('#') ? lower.slice(1) : lower;
  if (/^[0-9a-f]{6}$/.test(hex)) {
    return [
      Number.parseInt(hex.slice(0, 2), 16),
      Number.parseInt(hex.slice(2, 4), 16),
      Number.parseInt(hex.slice(4, 6), 16),
    ];
  }
  return fallback;
}

export function fillBackground(width: number, height: number, bg: Rgb): Uint8ClampedArray {
  const image = new Uint8ClampedArray(width * height * 4);
  for (let i = 0; i < width * height; i += 1) {
    image[i * 4] = bg[0];
    image[i * 4 + 1] = bg[1];
    image[i * 4 + 2] = bg[2];
    image[i * 4 + 3] = 255;
  }
  return image;
}
