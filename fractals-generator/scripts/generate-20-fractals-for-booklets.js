#!/usr/bin/env node

/**
 * Generate 20 lightweight TikZ booklet mattes via scripts/export-fractals-tex.ts,
 * flatten into artifacts/booklet-mattes/, and rewrite matte.tex + Makefile there.
 * Raster exports use A4-portrait proportions (595x842 pdf points).
 */

/** How to use this file:
 * under <root> folder, run: 
 * npm run generate:booklet-mattes 
 * then 
 * make pdf in artifacts/booklet-matte
 * or
 * cd artifacts/booklet-matte; make pdf
 */

const fs = require('node:fs/promises');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const REPO_ROOT = path.join(__dirname, '..');
const OUT_DIR = path.join(REPO_ROOT, 'artifacts', 'booklet-mattes');
const GEN_DIR = path.join(OUT_DIR, '.gen');
const EXPORT_SCRIPT = path.join(REPO_ROOT, 'scripts', 'export-fractals-tex.ts');

/** A4 portrait in PDF points (ISO 210mm x 297mm), same proportions as LaTeX `a4paper`. */
const A4_PORTRAIT_W = 595;
const A4_PORTRAIT_H = 842;

/** @type {{ family: string, preset: string, slug: string, title: string, params?: Record<string, string> }[]} */
const TARGETS = [
  { family: 'ifs', preset: 'sierpinskiTriangleIFS', slug: 'sierpinski-triangle', title: 'Sierpinski triangle IFS',
    params: { ifsIterations: '3200', ifsDensity: '120' } },
  // Was Cantor dust: orthogonal L-system motif (dense line matte, recognizable from Koch-style rules).
  { family: 'lsystem', preset: 'crystal', slug: 'crystal-l-system', title: 'Crystal (L-system)',
    params: { lsIterations: '4', lsDistance: '2.7' } },
  // Hilbert TikZ bbox is wildly tall → looks empty when scaled; sieve is triangular and clearly fractal.
  { family: 'lsystem', preset: 'siepinskiSieve', slug: 'sierpinski-sieve', title: 'Sierpinski sieve (L-system)',
    params: { lsIterations: '5', lsDistance: '4.5' } },
  { family: 'ifs', preset: 'radial2', slug: 'radial-ifs-2', title: 'Radial IFS II',
    params: { ifsIterations: '3400', ifsDensity: '76' } },
  { family: 'ifs', preset: 'ifsPythagorasTree', slug: 'ifs-pythagoras-tree', title: 'IFS Pythagoras tree',
    params: { ifsIterations: '2800', ifsDensity: '100' } },

  { family: 'lsystem', preset: 'seg32Curve', slug: 'seg32-curve', title: '32-segment curve' },
  { family: 'lsystem', preset: 'boxFractal', slug: 'box-fractal', title: 'Box fractal' },
  { family: 'lsystem', preset: 'board', slug: 'board', title: 'Board' },
  { family: 'lsystem', preset: 'tiles', slug: 'tiles', title: 'Tiles' },
  { family: 'lsystem', preset: 'quadraticKochIsland', slug: 'quadratic-koch-island', title: 'Quadratic Koch island' },
  { family: 'lsystem', preset: 'kochSnowflake', slug: 'koch-snowflake', title: 'Koch snowflake',
    params: { lsIterations: '4', lsDistance: '4' } },
  { family: 'lsystem', preset: 'dragonCurve', slug: 'dragon-curve', title: 'Dragon curve',
    params: { lsIterations: '8', lsDistance: '6' } },
  // Was Levy C curve (often blank in PDF when scaling clipped): Moore curve renders reliably here.
  { family: 'lsystem', preset: 'mooreCurve', slug: 'moore-curve', title: 'Moore curve',
    params: { lsIterations: '5', lsDistance: '5.3' } },
  { family: 'lsystem', preset: 'pythagorasTree', slug: 'l-system-pythagoras-tree', title: 'L-system Pythagoras tree',
    params: { lsIterations: '5', lsDistance: '4' } },

  // Replaced escape-time + Newton raster mattes with line-only L-system curves (white fill + \\draw strokes in TikZ export).
  { family: 'lsystem', preset: 'sierpinskiArrowhead', slug: 'sierpinski-arrowhead', title: 'Sierpinski arrowhead',
    params: { lsIterations: '7', lsDistance: '6' } },
  { family: 'lsystem', preset: 'sierpinskiCurve', slug: 'sierpinski-curve', title: 'Sierpinski curve',
    params: { lsIterations: '4', lsDistance: '4' } },
  { family: 'lsystem', preset: 'peanoCurve', slug: 'peano-curve', title: 'Peano curve',
    params: { lsIterations: '3', lsDistance: '4.5' } },
  { family: 'lsystem', preset: 'cross', slug: 'cross-fractal', title: 'Cross fractal',
    params: { lsIterations: '4', lsDistance: '3' } },
  { family: 'lsystem', preset: 'quadraticSnowflake', slug: 'quadratic-snowflake-ls', title: 'Quadratic snowflake curve',
    params: { lsIterations: '4', lsDistance: '3.8' } },
  { family: 'lsystem', preset: 'lTree', slug: 'l-tree', title: 'L-tree',
    params: { lsIterations: '5', lsDistance: '4.2' } },
];

function familiesForCopy() {
  return new Map([
    ['ifs', 'ifs'],
    ['lsystem', 'lsystem'],
  ]);
}

function resolveTsxCli() {
  const tsxCliMjs = path.join(REPO_ROOT, 'node_modules', 'tsx', 'dist', 'cli.mjs');
  return tsxCliMjs;
}

/** Plain ASCII section headings; escape only specials that hurt LaTeX in \\section*. */
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
    '--family',
    row.family,
    '--preset',
    row.preset,
    '--format',
    'tikz',
    '--out',
    GEN_DIR,
    '--size',
    `${A4_PORTRAIT_W}x${A4_PORTRAIT_H}`,
    '--tex-max-dim',
    '112',
    '--scheme',
    'acu',
    '--bg',
    '#ffffff',
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
  lines.push('% Generated by scripts/generate-20-fractals-for-booklets.js');
  lines.push('% Figures use adjustbox so extreme-aspect L-systems stay on-page.');
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
    '# Generated by scripts/generate-20-fractals-for-booklets.js',
    'DIR := $(dir $(lastword $(MAKEFILE_LIST)))',
    '',
    '# `pdf.` accepts a common typo (sentence-ending period after the target).',
    '.PHONY: pdf pdf. clean',
    '',
    'pdf pdf.:',
    '\tcd "$(DIR)" && lualatex -interaction=nonstopmode matte.tex',
    '',
    'clean:',
    '\tcd "$(DIR)" && rm -f matte.aux matte.log matte.pdf',
    '',
    '',
  ].join('\n');
}

async function main() {
  await mkdirp(OUT_DIR);
  await rimraf(GEN_DIR);
  await mkdirp(GEN_DIR);

  let i = 0;
  const folders = familiesForCopy();
  const written = [];

  for (const row of TARGETS) {
    const argv = buildArgvRow(row);
    console.log(`[${String(i + 1).padStart(2, '0')}/20] export ${row.family}/${row.preset}`);
    runExporter(argv);
    const dst = await flattenCopy(i, row, folders);
    written.push(dst);
    i += 1;
  }

  await fs.writeFile(path.join(OUT_DIR, 'matte.tex'), writeMatteTex(), 'utf8');
  await fs.writeFile(path.join(OUT_DIR, 'Makefile'), writeMakefileBody(), 'utf8');
  console.log(`Wrote ${written.length} .tikz files, matte.tex, Makefile → ${OUT_DIR}`);
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});
