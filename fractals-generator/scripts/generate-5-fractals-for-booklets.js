#!/usr/bin/env node

/**
 * Generate 5 Mandelbrot-family booklet mattes via scripts/export-fractals-tex.ts,
 * flatten into artifacts/booklet-mattes-5/, and rewrite matte.tex + Makefile there.
 * Also renders direct PNGs using the server-side renderer (same as web API).
 * Raster exports use A4-portrait proportions (595x842 pdf points).
 *
 * Usage (from <root> folder):
 *   node scripts/generate-5-fractals-for-booklets.js
 * Then (if lualatex is available):
 *   cd artifacts/booklet-mattes-5; make pdf
 * PNGs are written directly to artifacts/booklet-mattes-5/.
 */

const fs = require('node:fs/promises');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const REPO_ROOT = path.join(__dirname, '..');
const OUT_DIR = path.join(REPO_ROOT, 'artifacts', 'booklet-mattes-5');
const GEN_DIR = path.join(OUT_DIR, '.gen');
const EXPORT_SCRIPT = path.join(REPO_ROOT, 'scripts', 'export-fractals-tex.ts');

const A4_PORTRAIT_W = 595;
const A4_PORTRAIT_H = 842;

/**
 * 15 Mandelbrot-family variants with different presets, color schemes, and settings.
 * Only 'acu' and 'matrix' produce meaningful gradients for escape-time fractals;
 * 'emerald' and 'ink' are solid colors designed for line-based drawings.
 */
const TARGETS = [
  // -- original 5 --
  {
    family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-classic',
    title: 'Mandelbrot Set (Classic)',
    scheme: 'acu',
    params: { etMaxIterations: '300' },
  },
  {
    family: 'escapeTime', preset: 'burningShip', slug: 'burning-ship',
    title: 'Burning Ship',
    scheme: 'acu',
    params: { etMaxIterations: '400' },
  },
  {
    family: 'escapeTime', preset: 'multibrot', slug: 'multibrot',
    title: 'Multibrot (d=3)',
    scheme: 'matrix',
    params: { etMaxIterations: '420', etPower: '3' },
  },
  {
    family: 'escapeTime', preset: 'juliaClassic', slug: 'julia-classic',
    title: 'Julia Set (c = -0.8 + 0.156i)',
    scheme: 'acu',
    params: { etMaxIterations: '350' },
  },
  {
    family: 'escapeTime', preset: 'mandelbrotDoubleHook', slug: 'mandelbrot-double-hook',
    title: 'Mandelbrot (Double Hook)',
    scheme: 'acu',
    params: { etMaxIterations: '600' },
  },

  // -- 10 new variants --
  {
    family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-matrix',
    title: 'Mandelbrot Set (Matrix Palette)',
    scheme: 'matrix',
    params: { etMaxIterations: '400' },
  },
  {
    family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-power4',
    title: 'Mandelbrot Set (d=4)',
    scheme: 'acu',
    params: { etMaxIterations: '300', etPower: '4' },
  },
  {
    family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-hiiter',
    title: 'Mandelbrot Set (800 Iterations)',
    scheme: 'acu',
    params: { etMaxIterations: '800' },
  },
  {
    family: 'escapeTime', preset: 'mandelbrot', slug: 'mandelbrot-loiter',
    title: 'Mandelbrot Set (150 Iterations)',
    scheme: 'acu',
    params: { etMaxIterations: '150' },
  },
  {
    family: 'escapeTime', preset: 'burningShip', slug: 'burning-ship-matrix',
    title: 'Burning Ship (Matrix Palette)',
    scheme: 'matrix',
    params: { etMaxIterations: '400' },
  },
  {
    family: 'escapeTime', preset: 'juliaClassic', slug: 'julia-dendrite',
    title: 'Julia Set (c = -0.4 + 0.6i)',
    scheme: 'acu',
    params: { etMaxIterations: '350', etJuliaRe: '-0.4', etJuliaIm: '0.6' },
  },
  {
    family: 'escapeTime', preset: 'juliaProbability', slug: 'julia-spiral',
    title: 'Julia Set (c = -0.7269 + 0.1889i)',
    scheme: 'acu',
    params: { etMaxIterations: '450', etJuliaRe: '-0.7269', etJuliaIm: '0.1889' },
  },
  {
    family: 'escapeTime', preset: 'juliaClassic', slug: 'julia-power3',
    title: 'Julia Set (d=3, c = -0.8 + 0.156i)',
    scheme: 'acu',
    params: { etMaxIterations: '300', etPower: '3' },
  },
  {
    family: 'escapeTime', preset: 'juliaVectors', slug: 'julia-matrix',
    title: 'Julia Set (Matrix, c = 0.285 + 0.01i)',
    scheme: 'matrix',
    params: { etMaxIterations: '350', etJuliaRe: '0.285', etJuliaIm: '0.01' },
  },
  {
    family: 'escapeTime', preset: 'juliaSequences', slug: 'julia-feather',
    title: 'Julia Set (c = -0.1 + 0.8i)',
    scheme: 'acu',
    params: { etMaxIterations: '400', etJuliaRe: '-0.1', etJuliaIm: '0.8' },
  },
];

function resolveTsxCli() {
  return path.join(REPO_ROOT, 'node_modules', 'tsx', 'dist', 'cli.mjs');
}

function escapeTexTitle(raw) {
  return raw.replace(/[&%#]/g, (ch) => `\\${ch}`);
}

async function mkdirp(dir) {
  await fs.mkdir(dir, { recursive: true });
}

function runExporter(argv) {
  const tsx = resolveTsxCli();
  const r = spawnSync(process.execPath, [tsx, EXPORT_SCRIPT, ...argv], {
    cwd: REPO_ROOT,
    stdio: 'inherit',
    encoding: 'utf8',
    env: { ...process.env },
  });
  if (r.error) throw r.error;
  if (r.status !== 0) throw new Error(`export-fractals-tex exited ${r.status}`);
}

async function rimraf(dir) {
  await fs.rm(dir, { recursive: true, force: true }).catch(() => {});
}

async function copyFile(from, to) {
  await fs.copyFile(from, to);
}

function buildArgvRow(row) {
  const base = [
    '--family', row.family,
    '--preset', row.preset,
    '--format', 'tikz',
    '--out', GEN_DIR,
    '--size', `${A4_PORTRAIT_W}x${A4_PORTRAIT_H}`,
    '--tex-max-dim', '250',
    '--scheme', row.scheme,
    '--bg', '#ffffff',
  ];
  const p = row.params ?? {};
  for (const [k, v] of Object.entries(p)) {
    base.push('--param', `${k}=${v}`);
  }
  return base;
}

function destTikzName(idx, slug) {
  const n = String(idx + 1).padStart(2, '0');
  return `${n}-${slug}.tikz`;
}

function familiesForCopy() {
  return new Map([['escapeTime', 'escapeTime']]);
}

async function flattenCopy(rowIdx, row, folders) {
  const folderKey = folders.get(row.family);
  if (!folderKey) throw new Error(`Unknown family slug: ${row.family}`);
  const src = path.join(GEN_DIR, folderKey, `${row.preset}.tikz`);
  const dst = path.join(OUT_DIR, destTikzName(rowIdx, row.slug));
  await copyFile(src, dst);
  return dst;
}

function writeMatteTex() {
  const lines = [];
  lines.push('% Generated by scripts/generate-5-fractals-for-booklets.js');
  lines.push('\\documentclass[11pt,a4paper]{article}');
  lines.push('\\usepackage{tikz}');
  lines.push('\\usepackage[margin=1.5cm]{geometry}');
  lines.push('\\usepackage{graphicx}');
  lines.push('\\usepackage{adjustbox}');
  lines.push('');
  lines.push('\\begin{document}');
  TARGETS.forEach((row, i) => {
    const fname = destTikzName(i, row.slug);
    const titleTex = escapeTexTitle(row.title);
    lines.push(`\\section*{${titleTex}}`);
    lines.push('\\begin{center}');
    lines.push(
      '\\adjustbox{max width=0.92\\linewidth,max height=0.72\\textheight,keepaspectratio,center}{',
    );
    lines.push(`\\input{${fname}}`);
    lines.push('}');
    lines.push('\\end{center}\\clearpage');
    lines.push('');
  });
  lines.push('\\end{document}');
  lines.push('');
  return lines.join('\n');
}

function writeMakefileBody() {
  return [
    '# Generated by scripts/generate-5-fractals-for-booklets.js',
    'DIR := $(dir $(lastword $(MAKEFILE_LIST)))',
    '',
    '.PHONY: pdf pdf. clean',
    '',
    'pdf pdf.:',
    '\tcd "$(DIR)" && lualatex -interaction=nonstopmode matte.tex',
    '',
    'clean:',
    '\tcd "$(DIR)" && rm -f matte.aux matte.log matte.pdf',
    '',
  ].join('\n');
}

// ---------- Direct PNG rendering (via tsx helper) ----------

async function renderPngs() {
  const tsx = resolveTsxCli();
  const helper = path.join(REPO_ROOT, 'scripts', 'render-5-fractals-png.ts');
  const r = spawnSync(process.execPath, [tsx, helper, OUT_DIR], {
    cwd: REPO_ROOT,
    stdio: 'inherit',
    encoding: 'utf8',
    env: { ...process.env },
  });
  if (r.error) throw r.error;
  if (r.status !== 0) throw new Error(`render-5-fractals-png.ts exited ${r.status}`);
}

// ---------- Main ----------

async function main() {
  await mkdirp(OUT_DIR);
  await rimraf(GEN_DIR);
  await mkdirp(GEN_DIR);

  const folders = familiesForCopy();
  const written = [];

  // Step 1: Generate TikZ files via export-fractals-tex.ts
  console.log('=== Generating TikZ files ===');
  for (let i = 0; i < TARGETS.length; i += 1) {
    const row = TARGETS[i];
    const argv = buildArgvRow(row);
    console.log(`[${String(i + 1).padStart(2, '0')}/${TARGETS.length}] export ${row.family}/${row.preset} (${row.scheme})`);
    runExporter(argv);
    const dst = await flattenCopy(i, row, folders);
    written.push(dst);
  }

  await fs.writeFile(path.join(OUT_DIR, 'matte.tex'), writeMatteTex(), 'utf8');
  await fs.writeFile(path.join(OUT_DIR, 'Makefile'), writeMakefileBody(), 'utf8');
  console.log(`Wrote ${written.length} .tikz files, matte.tex, Makefile → ${OUT_DIR}`);

  // Step 2: Render high-quality PNGs directly
  console.log('\n=== Rendering PNGs ===');
  await renderPngs();

  console.log(`\nDone. Output → ${OUT_DIR}`);
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});
