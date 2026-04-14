import { NextRequest, NextResponse } from 'next/server';
import { getAppPresets } from '../../lib/server-presets';

export const runtime = 'nodejs';

function gradientColor(t: number): [number, number, number] {
  const stops = [[9, 10, 38], [45, 78, 140], [98, 187, 255], [255, 236, 130], [255, 140, 66]];
  const clamped = Math.max(0, Math.min(1, t));
  const scaled = clamped * (stops.length - 1);
  const i = Math.floor(scaled);
  const f = scaled - i;
  const c1 = stops[i];
  const c2 = stops[Math.min(stops.length - 1, i + 1)];
  return [
    Math.round(c1[0] + (c2[0] - c1[0]) * f),
    Math.round(c1[1] + (c2[1] - c1[1]) * f),
    Math.round(c1[2] + (c2[2] - c1[2]) * f),
  ];
}

function setPixel(image: Uint8ClampedArray, width: number, x: number, y: number, r: number, g: number, b: number): void {
  const idx = (y * width + x) * 4;
  image[idx] = r;
  image[idx + 1] = g;
  image[idx + 2] = b;
  image[idx + 3] = 255;
}

function mapPixelToComplex(
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

function renderEscapeTime(width: number, height: number, preset: any, params: any): Uint8ClampedArray {
  const image = new Uint8ClampedArray(width * height * 4).fill(255);
  const maxIterations = Number(params.etMaxIterations ?? preset.defaults.maxIterations);
  const bailout = Number(params.etBailout ?? preset.defaults.bailout);
  const power = Number(params.etPower ?? preset.defaults.power);
  const cRe = Number(params.etJuliaRe ?? preset.defaults.cRe);
  const cIm = Number(params.etJuliaIm ?? preset.defaults.cIm);
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const [u, v] = mapPixelToComplex(x, y, width, height, preset.viewport);
      let zr = preset.type === 'julia' ? u : 0;
      let zi = preset.type === 'julia' ? v : 0;
      const cr = preset.type === 'julia' ? cRe : u;
      const ci = preset.type === 'julia' ? cIm : v;
      let iter = 0;
      for (; iter < maxIterations; iter += 1) {
        let ar = zr;
        let ai = zi;
        if (preset.type === 'burning-ship') {
          ar = Math.abs(ar);
          ai = Math.abs(ai);
        }
        let nextR = 0;
        let nextI = 0;
        if (power === 2) {
          nextR = ar * ar - ai * ai + cr;
          nextI = 2 * ar * ai + ci;
        } else {
          const mag = Math.sqrt(ar * ar + ai * ai);
          const angle = Math.atan2(ai, ar);
          const magPow = mag ** power;
          nextR = magPow * Math.cos(power * angle) + cr;
          nextI = magPow * Math.sin(power * angle) + ci;
        }
        zr = nextR;
        zi = nextI;
        if (zr * zr + zi * zi > bailout * bailout) break;
      }
      if (iter >= maxIterations) {
        setPixel(image, width, x, y, 6, 7, 15);
      } else {
        const [r, g, b] = gradientColor(iter / maxIterations);
        setPixel(image, width, x, y, r, g, b);
      }
    }
  }
  return image;
}

function closestRootIndex(zr: number, zi: number, roots: Array<[number, number]>): number {
  let idx = 0;
  let best = Number.POSITIVE_INFINITY;
  for (let i = 0; i < roots.length; i += 1) {
    const dr = zr - roots[i][0];
    const di = zi - roots[i][1];
    const d2 = dr * dr + di * di;
    if (d2 < best) {
      best = d2;
      idx = i;
    }
  }
  return idx;
}

function renderNewton(width: number, height: number, preset: any, params: any): Uint8ClampedArray {
  const image = new Uint8ClampedArray(width * height * 4).fill(255);
  const maxIterations = Number(params.ntMaxIterations ?? preset.defaults.maxIterations);
  const epsilon = Number(params.ntEpsilon ?? preset.defaults.epsilon);
  const roots = preset.type === 'newton-cubic'
    ? [[1, 0], [-0.5, Math.sqrt(3) / 2], [-0.5, -Math.sqrt(3) / 2]]
    : [[1, 0], [0, 1], [-1, 0], [0, -1]];
  const palette = [[239, 68, 68], [59, 130, 246], [34, 197, 94], [234, 179, 8]];
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      let [zr, zi] = mapPixelToComplex(x, y, width, height, preset.viewport);
      let iter = 0;
      for (; iter < maxIterations; iter += 1) {
        let fr = 0; let fi = 0; let dfr = 0; let dfi = 0;
        const z2r = zr * zr - zi * zi;
        const z2i = 2 * zr * zi;
        if (preset.type === 'newton-cubic') {
          const z3r = z2r * zr - z2i * zi;
          const z3i = z2r * zi + z2i * zr;
          fr = z3r - 1; fi = z3i; dfr = 3 * z2r; dfi = 3 * z2i;
        } else {
          const z3r = z2r * zr - z2i * zi;
          const z3i = z2r * zi + z2i * zr;
          const z4r = z2r * z2r - z2i * z2i;
          const z4i = 2 * z2r * z2i;
          fr = z4r - 1; fi = z4i; dfr = 4 * z3r; dfi = 4 * z3i;
        }
        const denom = dfr * dfr + dfi * dfi;
        if (denom < 1e-14) break;
        const qr = (fr * dfr + fi * dfi) / denom;
        const qi = (fi * dfr - fr * dfi) / denom;
        zr -= qr; zi -= qi;
        if (qr * qr + qi * qi < epsilon * epsilon) break;
      }
      const rootIndex = closestRootIndex(zr, zi, roots as Array<[number, number]>);
      const base = palette[rootIndex % palette.length];
      const shade = 0.35 + 0.65 * (1 - iter / maxIterations);
      setPixel(image, width, x, y, Math.round(base[0] * shade), Math.round(base[1] * shade), Math.round(base[2] * shade));
    }
  }
  return image;
}

function renderDensityField(
  width: number,
  height: number,
  iterations: number,
  discard: number,
  initialState: { x: number; y: number; z: number },
  iterFn: (state: { x: number; y: number; z: number }) => { x: number; y: number; z: number },
  project: (s: { x: number; y: number; z: number }) => [number, number],
): Uint8ClampedArray {
  const hist = new Uint32Array(width * height);
  let state = { ...initialState };
  let minX = Number.POSITIVE_INFINITY; let minY = Number.POSITIVE_INFINITY;
  let maxX = Number.NEGATIVE_INFINITY; let maxY = Number.NEGATIVE_INFINITY;
  for (let i = 0; i < iterations; i += 1) {
    state = iterFn(state);
    if (!Number.isFinite(state.x) || !Number.isFinite(state.y) || !Number.isFinite(state.z)) {
      state = { ...initialState };
      continue;
    }
    if (i < discard) continue;
    const [x, y] = project(state);
    minX = Math.min(minX, x); maxX = Math.max(maxX, x);
    minY = Math.min(minY, y); maxY = Math.max(maxY, y);
  }
  if (!Number.isFinite(minX) || !Number.isFinite(minY) || !Number.isFinite(maxX) || !Number.isFinite(maxY)) {
    return renderFallbackField(width, height);
  }
  state = { ...initialState };
  const scaleX = (width - 1) / Math.max(1e-9, maxX - minX);
  const scaleY = (height - 1) / Math.max(1e-9, maxY - minY);
  let maxCount = 0;
  for (let i = 0; i < iterations; i += 1) {
    state = iterFn(state);
    if (!Number.isFinite(state.x) || !Number.isFinite(state.y) || !Number.isFinite(state.z)) {
      state = { ...initialState };
      continue;
    }
    if (i < discard) continue;
    const [x, y] = project(state);
    const px = Math.floor((x - minX) * scaleX);
    const py = Math.floor((maxY - y) * scaleY);
    if (px < 0 || py < 0 || px >= width || py >= height) continue;
    const idx = py * width + px;
    hist[idx] += 1;
    if (hist[idx] > maxCount) maxCount = hist[idx];
  }
  if (maxCount === 0) {
    return renderFallbackField(width, height);
  }
  const image = new Uint8ClampedArray(width * height * 4).fill(255);
  for (let py = 0; py < height; py += 1) {
    for (let px = 0; px < width; px += 1) {
      const count = hist[py * width + px];
      if (count === 0) continue;
      const [r, g, b] = gradientColor(Math.log(count + 1) / Math.log(maxCount + 1));
      setPixel(image, width, px, py, r, g, b);
    }
  }
  return image;
}

function renderAttractor(width: number, height: number, preset: any, params: any): Uint8ClampedArray {
  if (preset.type === 'ikeda') {
    return renderFallbackField(width, height);
  }
  const iterations = Number(params.atIterations ?? preset.defaults.iterations);
  const discard = Number(params.atDiscard ?? preset.defaults.discard);
  const a = Number(params.atA ?? preset.defaults.a);
  const b = Number(params.atB ?? preset.defaults.b);
  const c = Number(params.atC ?? preset.defaults.c);
  const d = Number(params.atD ?? preset.defaults.d);
  const iterFn = (state: { x: number; y: number; z: number }): { x: number; y: number; z: number } => {
    if (preset.type === 'clifford') return { x: Math.sin(a * state.y) + c * Math.cos(a * state.x), y: Math.sin(b * state.x) + d * Math.cos(b * state.y), z: state.z };
    if (preset.type === 'peter-de-jong') return { x: Math.sin(a * state.y) - Math.cos(b * state.x), y: Math.sin(c * state.x) - Math.cos(d * state.y), z: state.z };
    if (preset.type === 'henon') return { x: 1 - a * state.x * state.x + state.y, y: b * state.x, z: state.z };
    if (preset.type === 'ikeda') {
      const t = 0.4 - 6 / (1 + state.x * state.x + state.y * state.y);
      return { x: 1 + a * (state.x * Math.cos(t) - state.y * Math.sin(t)), y: a * (state.x * Math.sin(t) + state.y * Math.cos(t)), z: state.z };
    }
    if (preset.type === 'hopalong') {
      const sign = state.x < 0 ? -1 : 1;
      return { x: state.y - sign * Math.sqrt(Math.abs(b * state.x - c)), y: a - state.x, z: state.z };
    }
    const dt = d || 0.005;
    return { x: state.x + a * (state.y - state.x) * dt, y: state.y + (state.x * (b - state.z) - state.y) * dt, z: state.z + (state.x * state.y - c * state.z) * dt };
  };
  const project = preset.type === 'lorenz'
    ? (state: { x: number; y: number; z: number }): [number, number] => [state.x, state.z]
    : (state: { x: number; y: number; z: number }): [number, number] => [state.x, state.y];
  const initialState = preset.type === 'lorenz' || preset.type === 'ikeda'
    ? { x: 0.1, y: 0, z: 0 }
    : { x: 0, y: 0, z: 0 };
  return renderDensityField(width, height, iterations, discard, initialState, iterFn, project);
}

function renderFallbackField(width: number, height: number): Uint8ClampedArray {
  const fallback = new Uint8ClampedArray(width * height * 4).fill(255);
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const v = Math.abs(Math.sin((x / width) * 8) * Math.cos((y / height) * 11));
      if (v < 0.65) continue;
      const [r, g, b] = gradientColor(v);
      setPixel(fallback, width, x, y, r, g, b);
    }
  }
  return fallback;
}

function invertPoint(point: { x: number; y: number }, circle: { x: number; y: number; r: number }): { x: number; y: number } | null {
  const dx = point.x - circle.x;
  const dy = point.y - circle.y;
  const d2 = dx * dx + dy * dy;
  if (d2 < 1e-14) return null;
  const scale = (circle.r * circle.r) / d2;
  return { x: circle.x + dx * scale, y: circle.y + dy * scale };
}

function composeInversions(
  point: { x: number; y: number },
  first: { x: number; y: number; r: number },
  second: { x: number; y: number; r: number },
): { x: number; y: number } | null {
  const once = invertPoint(point, first);
  if (!once) return null;
  return invertPoint(once, second);
}

function renderKleinian(width: number, height: number, preset: any): Uint8ClampedArray {
  const iterations = Math.max(1000, Math.round(preset.defaults.iterations ?? 300000));
  const discard = Math.max(0, Math.round(preset.defaults.discard ?? 80));
  const circles = preset.defaults.circles;
  const generators = [
    (point: { x: number; y: number }) => composeInversions(point, circles[0], circles[1]),
    (point: { x: number; y: number }) => composeInversions(point, circles[1], circles[0]),
    (point: { x: number; y: number }) => composeInversions(point, circles[2], circles[3]),
    (point: { x: number; y: number }) => composeInversions(point, circles[3], circles[2]),
  ];
  const inverseGenerator = [1, 0, 3, 2];
  const points: Array<[number, number]> = [];
  let minX = Number.POSITIVE_INFINITY; let minY = Number.POSITIVE_INFINITY;
  let maxX = Number.NEGATIVE_INFINITY; let maxY = Number.NEGATIVE_INFINITY;
  let point = { x: preset.defaults.seed?.x ?? 0.02, y: preset.defaults.seed?.y ?? 0.01 };
  let previousGenerator = -1;
  for (let i = 0; i < iterations + discard; i += 1) {
    let generatorIndex = Math.floor(Math.random() * generators.length);
    if (previousGenerator >= 0) {
      while (generatorIndex === inverseGenerator[previousGenerator]) {
        generatorIndex = Math.floor(Math.random() * generators.length);
      }
    }
    const next = generators[generatorIndex](point);
    previousGenerator = generatorIndex;
    if (!next || !Number.isFinite(next.x) || !Number.isFinite(next.y)) {
      point = { x: 0.02, y: 0.02 };
      previousGenerator = -1;
      continue;
    }
    point = next;
    if (i < discard) continue;
    points.push([point.x, point.y]);
    minX = Math.min(minX, point.x); maxX = Math.max(maxX, point.x);
    minY = Math.min(minY, point.y); maxY = Math.max(maxY, point.y);
  }
  const hist = new Uint32Array(width * height);
  let maxCount = 0;
  const pad = 0.03;
  const spanX = Math.max(1e-9, maxX - minX);
  const spanY = Math.max(1e-9, maxY - minY);
  const loX = minX - spanX * pad;
  const hiX = maxX + spanX * pad;
  const loY = minY - spanY * pad;
  const hiY = maxY + spanY * pad;
  for (let i = 0; i < points.length; i += 1) {
    const x = points[i][0];
    const y = points[i][1];
    const px = Math.floor(((x - loX) / (hiX - loX)) * (width - 1));
    const py = Math.floor(((hiY - y) / (hiY - loY)) * (height - 1));
    if (px < 0 || py < 0 || px >= width || py >= height) continue;
    const idx = py * width + px;
    hist[idx] += 1;
    if (hist[idx] > maxCount) maxCount = hist[idx];
  }
  const image = new Uint8ClampedArray(width * height * 4).fill(255);
  for (let py = 0; py < height; py += 1) {
    for (let px = 0; px < width; px += 1) {
      const value = hist[py * width + px];
      if (value === 0) continue;
      const [r, g, b] = gradientColor(Math.log(value + 1) / Math.log(maxCount + 1));
      setPixel(image, width, px, py, r, g, b);
    }
  }
  return image;
}

function renderInversion(width: number, height: number, preset: any): Uint8ClampedArray {
  if (preset.type === 'apollonian-gasket' || preset.type === 'kleinian-schottky') {
    return renderFallbackField(width, height);
  }
  return new Uint8ClampedArray(width * height * 4).fill(255);
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  const body = await request.json();
  const family = String(body.family) as keyof ReturnType<typeof getAppPresets>;
  const presetKey = String(body.preset);
  const width = Number(body.width ?? 980);
  const height = Number(body.height ?? 760);
  const params = body.params ?? {};
  const presets = getAppPresets();
  const preset = presets[family]?.[presetKey];
  if (!preset) {
    return NextResponse.json({ error: `Unknown preset ${family}/${presetKey}` }, { status: 400 });
  }
  let image: Uint8ClampedArray;
  if (family === 'escapeTime') image = renderEscapeTime(width, height, preset, params);
  else if (family === 'newton') image = renderNewton(width, height, preset, params);
  else if (family === 'attractor') image = renderAttractor(width, height, preset, params);
  else if (family === 'inversion') image = renderInversion(width, height, preset);
  else image = new Uint8ClampedArray(width * height * 4).fill(255);
  return NextResponse.json({ image: Array.from(image), meta: `Rendered ${family}/${presetKey}` });
}
