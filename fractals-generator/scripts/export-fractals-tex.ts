#!/usr/bin/env npx tsx
/**
 * CLI: export fractals as TikZ snippets and/or standalone LaTeX.
 * Reuses app/lib/server-export-tex (same logic as the web API).
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { exportFractalTex } from '../app/lib/server-export-tex';
import { getAppPresets } from '../app/lib/server-presets';
import { parseColor, resolveFractalFamily } from '../app/lib/server-render-utils';
import type { FractalType } from '../app/types';

const FAMILIES: FractalType[] = ['ifs', 'lsystem', 'escapeTime', 'newton', 'attractor', 'inversion'];

const DEFAULT_PRESET: Record<FractalType, string> = {
  ifs: 'fern',
  lsystem: 'pythagorasTree',
  escapeTime: 'mandelbrot',
  newton: 'newtonCubic',
  attractor: 'clifford',
  inversion: 'apollonianGasket',
};

const DEFAULT_WIDTH = 1280;
const DEFAULT_HEIGHT = 720;

type CliFormat = 'tikz' | 'tex' | 'both';

type CliOptions = {
  help?: boolean;
  family?: string;
  preset?: string;
  format: CliFormat;
  outDir: string;
  width: number;
  height: number;
  mainColorScheme: string;
  backgroundColor: string;
  texMaxDim?: number;
  extraParams: Record<string, string>;
};

function printHelp(): void {
  console.log(
    [
      'Export fractals as TikZ (.tikz) and/or standalone LaTeX (.tex).',
      '',
      'Usage:',
      '  npx tsx scripts/export-fractals-tex.ts [options]',
      '',
      'Default mode (no --family / --preset):',
      '  Exports one default preset per fractal family.',
      '',
      'Options:',
      '  --help, -h              Show this message',
      '  --family <name|all>     ifs | lsystem | escape-time | newton | attractor | inversion | all',
      '  --preset <key|all>     Preset key within the family, or all',
      '  --format <tikz|tex|both>  Output kind (default: both)',
      '  --out <dir>            Output directory (default: artifacts/tex)',
      '  --width <px>           Reference width (default: 1280)',
      '  --height <px>          Reference height (default: 720)',
      '  --size <WxH>           Shorthand for width and height',
      '  --scheme <name>        mainColorScheme: acu | matrix | emerald | ink (default: acu)',
      '  --bg <hex>             Background #RRGGBB (default: #ffffff)',
      '  --tex-max-dim <n>      Max raster dimension for escape/newton/attractor/inversion',
      '  --param key=value      Extra render params (repeatable), same keys as the web API',
      '',
      'Examples:',
      '  npx tsx scripts/export-fractals-tex.ts',
      '  npx tsx scripts/export-fractals-tex.ts --family ifs --preset fern --format tex --out ./out',
      '  npx tsx scripts/export-fractals-tex.ts --family lsystem --preset all --format tikz',
      '  npx tsx scripts/export-fractals-tex.ts --param ifsIterations=80000 --param ifsDensity=70',
    ].join('\n'),
  );
}

function parseArgs(argv: string[]): CliOptions {
  const options: CliOptions = {
    format: 'both',
    outDir: path.resolve(process.cwd(), 'artifacts/tex'),
    width: DEFAULT_WIDTH,
    height: DEFAULT_HEIGHT,
    mainColorScheme: 'acu',
    backgroundColor: '#ffffff',
    extraParams: {},
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === '--help' || arg === '-h') {
      options.help = true;
      return options;
    }

    if (arg === '--family') {
      options.family = String(argv[i + 1] ?? '');
      i += 1;
      continue;
    }

    if (arg === '--preset') {
      options.preset = String(argv[i + 1] ?? '');
      i += 1;
      continue;
    }

    if (arg === '--format') {
      const v = String(argv[i + 1] ?? '').toLowerCase();
      i += 1;
      if (v === 'tikz' || v === 'tex' || v === 'both') options.format = v;
      else throw new Error(`Invalid --format: ${v}`);
      continue;
    }

    if (arg === '--out') {
      options.outDir = path.resolve(process.cwd(), argv[i + 1] ?? '');
      i += 1;
      continue;
    }

    if (arg === '--width') {
      options.width = Number(argv[i + 1]);
      i += 1;
      continue;
    }

    if (arg === '--height') {
      options.height = Number(argv[i + 1]);
      i += 1;
      continue;
    }

    if (arg === '--size') {
      const value = String(argv[i + 1] ?? '');
      i += 1;
      const [w, h] = value.toLowerCase().split('x').map(Number);
      options.width = w;
      options.height = h;
      continue;
    }

    if (arg === '--scheme') {
      options.mainColorScheme = String(argv[i + 1] ?? 'acu');
      i += 1;
      continue;
    }

    if (arg === '--bg') {
      options.backgroundColor = String(argv[i + 1] ?? '#ffffff');
      i += 1;
      continue;
    }

    if (arg === '--tex-max-dim') {
      options.texMaxDim = Number.parseInt(String(argv[i + 1] ?? ''), 10);
      i += 1;
      continue;
    }

    if (arg === '--param') {
      const raw = String(argv[i + 1] ?? '');
      i += 1;
      const eq = raw.indexOf('=');
      if (eq <= 0) throw new Error(`Invalid --param (expected key=value): ${raw}`);
      const k = raw.slice(0, eq).trim();
      const v = raw.slice(eq + 1).trim();
      options.extraParams[k] = v;
      continue;
    }

    throw new Error(`Unknown argument: ${arg}`);
  }

  if (!Number.isFinite(options.width) || options.width <= 0) {
    throw new Error('width must be a positive number');
  }
  if (!Number.isFinite(options.height) || options.height <= 0) {
    throw new Error('height must be a positive number');
  }
  options.width = Math.round(options.width);
  options.height = Math.round(options.height);

  return options;
}

function normalizeFamilyInput(raw: string): FractalType | 'all' | null {
  const s = raw.trim().toLowerCase();
  if (s === 'all') return 'all';
  return resolveFractalFamily(s);
}

type Target = { family: FractalType; presetKey: string };

function buildTargets(options: CliOptions, presets: ReturnType<typeof getAppPresets>): Target[] {
  const famRaw = options.family;
  const presetRaw = options.preset;

  if (!famRaw && !presetRaw) {
    return FAMILIES.map((family) => ({ family, presetKey: DEFAULT_PRESET[family] }));
  }

  if (presetRaw && !famRaw) {
    throw new Error('When using --preset, also pass --family (or use default mode with neither flag).');
  }

  const family = normalizeFamilyInput(famRaw ?? '');
  if (!family) {
    throw new Error(`Unknown family: ${famRaw}`);
  }

  if (family === 'all') {
    if (!presetRaw) {
      return FAMILIES.map((f) => ({ family: f, presetKey: DEFAULT_PRESET[f] }));
    }
    if (presetRaw.toLowerCase() === 'all') {
      const out: Target[] = [];
      for (const f of FAMILIES) {
        for (const key of Object.keys(presets[f] ?? {})) {
          out.push({ family: f, presetKey: key });
        }
      }
      return out;
    }
    const targets: Target[] = [];
    for (const f of FAMILIES) {
      if (presets[f]?.[presetRaw]) targets.push({ family: f, presetKey: presetRaw });
    }
    if (!targets.length) throw new Error(`Preset "${presetRaw}" not found in any family.`);
    return targets;
  }

  const famPresets = presets[family];
  if (!famPresets) throw new Error(`No presets for family ${family}`);

  if (!presetRaw) {
    return [{ family, presetKey: DEFAULT_PRESET[family] }];
  }

  if (presetRaw.toLowerCase() === 'all') {
    return Object.keys(famPresets).map((presetKey) => ({ family, presetKey }));
  }

  if (!famPresets[presetRaw]) {
    throw new Error(`Unknown preset ${family}/${presetRaw}`);
  }
  return [{ family, presetKey: presetRaw }];
}

async function main(): Promise<void> {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  const presets = getAppPresets();
  const targets = buildTargets(options, presets);
  const bg = parseColor(options.backgroundColor, [255, 255, 255]);
  const texOpts =
    options.texMaxDim !== undefined && Number.isFinite(options.texMaxDim)
      ? { rasterMaxDim: Math.max(32, Math.min(4096, Math.round(options.texMaxDim))) }
      : {};

  await fs.mkdir(options.outDir, { recursive: true });

  for (const { family, presetKey } of targets) {
    const preset = presets[family]?.[presetKey];
    if (!preset) {
      console.warn(`Skip missing ${family}/${presetKey}`);
      continue;
    }
    const params: Record<string, string> = { ...options.extraParams };
    const subdir = path.join(options.outDir, family);
    await fs.mkdir(subdir, { recursive: true });
    const basePath = path.join(subdir, presetKey);

    if (options.format === 'tikz' || options.format === 'both') {
      const body = exportFractalTex(
        family,
        options.width,
        options.height,
        preset,
        params,
        options.mainColorScheme,
        bg,
        'tikz',
        texOpts,
      );
      await fs.writeFile(`${basePath}.tikz`, body, 'utf8');
      console.log(`Wrote ${basePath}.tikz`);
    }
    if (options.format === 'tex' || options.format === 'both') {
      const body = exportFractalTex(
        family,
        options.width,
        options.height,
        preset,
        params,
        options.mainColorScheme,
        bg,
        'standalone',
        texOpts,
      );
      await fs.writeFile(`${basePath}.tex`, body, 'utf8');
      console.log(`Wrote ${basePath}.tex`);
    }
  }

  console.log(`Done. ${targets.length} preset(s) → ${options.outDir}`);
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exitCode = 1;
});
