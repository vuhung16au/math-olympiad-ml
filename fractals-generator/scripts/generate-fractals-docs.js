#!/usr/bin/env node

const fs = require('node:fs/promises');
const path = require('node:path');

const {
  IFS_PRESETS,
  LSYSTEM_PRESETS,
  ESCAPE_TIME_PRESETS,
  NEWTON_PRESETS,
  ATTRACTOR_PRESETS,
  INVERSION_PRESETS,
  slugify,
} = require('./generate-all-fractals');

function formatSettings(settings) {
  return Object.entries(settings)
    .map(([k, v]) => `${k}=${v}`)
    .join(', ');
}

function formatRulesInline(rules) {
  return Object.entries(rules)
    .map(([k, v]) => `${k} -> ${v}`)
    .join(', ');
}

function buildIFSSection() {
  const lines = ['## IFS Presets', ''];

  for (const preset of Object.values(IFS_PRESETS)) {
    const image = `../artifacts/ifs/${slugify(preset.label)}.png`;
    const math = preset.equation === 'radial' ? 'Radial IFS' : 'Affine IFS';
    const params = preset.equation === 'radial'
      ? '`matrices=[{a,b,t,e,f,p}...]`, `equation=radial`'
      : '`matrices=[{a,b,c,d,e,f,p}...]`';

    lines.push(`### ${preset.label}`);
    lines.push('');
    lines.push(`![${preset.label}](${image})`);
    lines.push('');
    lines.push(`- Math definition: ${math}`);
    lines.push(`- Settings (default): \`${formatSettings(preset.defaults)}\``);
    lines.push(`- Params: ${params}`);
    lines.push('');
  }

  return lines;
}

function buildLSystemSection() {
  const lines = ['## L-system Presets', ''];

  for (const preset of Object.values(LSYSTEM_PRESETS)) {
    const image = `../artifacts/lsystem/${slugify(preset.label)}.png`;
    const rulesInline = formatRulesInline(preset.rules);

    lines.push(`### ${preset.label}`);
    lines.push('');
    lines.push(`![${preset.label}](${image})`);
    lines.push('');
    lines.push(`- Math definition: L-system with \`axiom=${preset.axiom}\`, ${rulesInline}`);
    lines.push(`- Settings (default): \`${formatSettings(preset.defaults)}\``);
    lines.push('');
  }

  return lines;
}

function buildEscapeTimeSection() {
  const lines = ['## Escape-time Presets', ''];

  for (const preset of Object.values(ESCAPE_TIME_PRESETS)) {
    const image = `../artifacts/escape-time/${slugify(preset.label)}.png`;
    let math = '`z_{n+1} = z_n^2 + c`';
    if (preset.type === 'burning-ship') {
      math = '`z_{n+1} = (|Re(z_n)| + i|Im(z_n)|)^2 + c`';
    } else if (preset.power && preset.power !== 2) {
      math = `\`z_{n+1} = z_n^${preset.power} + c\``;
    }

    lines.push(`### ${preset.label}`);
    lines.push('');
    lines.push(`![${preset.label}](${image})`);
    lines.push('');
    lines.push(`- Math definition: ${math}`);
    lines.push(`- Settings (default): \`viewport=[${preset.viewport.minX}, ${preset.viewport.maxX}] x [${preset.viewport.minY}, ${preset.viewport.maxY}], maxIterations=${preset.maxIterations}, bailout=${preset.bailout ?? 4}\``);
    lines.push('');
  }

  return lines;
}

function buildNewtonSection() {
  const lines = ['## Newton Presets', ''];

  for (const preset of Object.values(NEWTON_PRESETS)) {
    const image = `../artifacts/newton/${slugify(preset.label)}.png`;
    const polynomial = preset.type === 'newton-cubic' ? '`p(z)=z^3-1`' : '`p(z)=z^4-1`';

    lines.push(`### ${preset.label}`);
    lines.push('');
    lines.push(`![${preset.label}](${image})`);
    lines.push('');
    lines.push(`- Math definition: Newton iteration \`z_{n+1} = z_n - p(z_n)/p'(z_n)\` with ${polynomial}`);
    lines.push(`- Settings (default): \`viewport=[${preset.viewport.minX}, ${preset.viewport.maxX}] x [${preset.viewport.minY}, ${preset.viewport.maxY}], maxIterations=${preset.maxIterations}, epsilon=${preset.epsilon}\``);
    lines.push('');
  }

  return lines;
}

function buildAttractorSection() {
  const lines = ['## Strange Attractor Presets', ''];

  for (const preset of Object.values(ATTRACTOR_PRESETS)) {
    const image = `../artifacts/attractors/${slugify(preset.label)}.png`;
    let math = '`x_{n+1} = sin(a y_n) + c cos(a x_n), y_{n+1} = sin(b x_n) + d cos(b y_n)`';
    if (preset.type === 'peter-de-jong') {
      math = '`x_{n+1} = sin(a y_n) - cos(b x_n), y_{n+1} = sin(c x_n) - cos(d y_n)`';
    }

    lines.push(`### ${preset.label}`);
    lines.push('');
    lines.push(`![${preset.label}](${image})`);
    lines.push('');
    lines.push(`- Math definition: ${math}`);
    lines.push(`- Settings (default): \`${formatSettings({ ...preset.params, iterations: preset.iterations, discard: preset.discard })}\``);
    lines.push('');
  }

  return lines;
}

function buildInversionSection() {
  const lines = ['## Circle Inversion Presets', ''];

  for (const preset of Object.values(INVERSION_PRESETS)) {
    const image = `../artifacts/inversions/${slugify(preset.label)}.png`;

    lines.push(`### ${preset.label}`);
    lines.push('');
    lines.push(`![${preset.label}](${image})`);
    lines.push('');
    if (preset.type === 'apollonian-gasket') {
      lines.push('- Math definition: Circle inversion / Descartes recursion for tangent circles');
      lines.push(`- Settings (default): \`depth=${preset.depth}, minRadius=${preset.minRadius}\``);
    } else {
      lines.push('- Math definition: Kleinian (Schottky) group generated by compositions of circle inversions (Mobius maps)');
      lines.push(`- Settings (default): \`iterations=${preset.iterations}, discard=${preset.discard}, viewport=[${preset.viewport.minX}, ${preset.viewport.maxX}] x [${preset.viewport.minY}, ${preset.viewport.maxY}]\``);
    }
    lines.push('');
  }

  return lines;
}

function buildDocument() {
  const lines = [
    '# Fractals Catalog',
    '',
    'This library generates fractals with six families:',
    '',
    '- IFS (Iterated Function Systems)',
    '- L-system (Lindenmayer systems)',
    '- Escape-time fractals (complex dynamics)',
    '- Newton fractals',
    '- Strange attractors',
    '- Circle inversion fractals',
    '',
    'All sample images below are generated by `scripts/generate-all-fractals.js` and stored in `artifacts/`.',
    '',
    '## Common Math',
    '',
    '### IFS (Affine)',
    '',
    'At each iteration, choose transform `i` with probability `p_i` and apply:',
    '',
    '$$',
    '\\begin{aligned}',
    'x_{n+1} &= a_i x_n + b_i y_n + e_i \\\\',
    'y_{n+1} &= c_i x_n + d_i y_n + f_i',
    '\\end{aligned}',
    '$$',
    '',
    '### IFS (Radial)',
    '',
    'For radial presets, use:',
    '',
    '$$',
    '\\begin{aligned}',
    'x_{n+1} &= a_i x_n \\cos(t_i) - b_i y_n \\sin(t_i) + e_i \\\\',
    'y_{n+1} &= a_i x_n \\sin(t_i) + b_i y_n \\cos(t_i) + f_i',
    '\\end{aligned}',
    '$$',
    '',
    '### L-system + Turtle Rules',
    '',
    'String rewriting:',
    '',
    '$$',
    '\\omega_{k+1} = P(\\omega_k)',
    '$$',
    '',
    'Turtle interpretation used in this project:',
    '',
    '- `F`: move and draw',
    '- `B`: move backward and draw',
    '- `+`: turn right by `angle`',
    '- `-`: turn left by `angle`',
    '- `[`: push state',
    '- `]`: pop state',
    '- `<` / `>`: scale line length',
    '',
    'Forward step update:',
    '',
    '$$',
    '\\begin{aligned}',
    'x_{n+1} &= x_n - d\\sin(\\theta_n) \\\\',
    'y_{n+1} &= y_n + d\\cos(\\theta_n)',
    '\\end{aligned}',
    '$$',
    '',
    '### Escape-time (Complex Dynamics)',
    '',
    'Per-pixel recurrence, color by escape iteration:',
    '',
    '$$',
    'z_{n+1}=f(z_n,c),\\quad |z_n|>R \\Rightarrow \\text{escape}',
    '$$',
    '',
    '### Newton Fractals',
    '',
    '$$',
    "z_{n+1}=z_n-\\frac{p(z_n)}{p'(z_n)}",
    '$$',
    '',
    '### Strange Attractors',
    '',
    'Iterated chaotic maps in 2D, rendered as density plots.',
    '',
    '### Circle Inversions',
    '',
    'Inversion around circles; for Apollonian gaskets, recursively fill tangent circles.',
    '',
    '---',
    '',
  ];

  lines.push(...buildIFSSection());
  lines.push('---', '');
  lines.push(...buildLSystemSection());
  lines.push('---', '');
  lines.push(...buildEscapeTimeSection());
  lines.push('---', '');
  lines.push(...buildNewtonSection());
  lines.push('---', '');
  lines.push(...buildAttractorSection());
  lines.push('---', '');
  lines.push(...buildInversionSection());

  return `${lines.join('\n')}\n`;
}

async function main() {
  const outPath = path.resolve(process.cwd(), 'docs/fractals.md');
  const content = buildDocument();
  await fs.mkdir(path.dirname(outPath), { recursive: true });
  await fs.writeFile(outPath, content);
  console.log(`Generated ${outPath}`);
  console.log(`IFS presets: ${Object.keys(IFS_PRESETS).length}`);
  console.log(`L-system presets: ${Object.keys(LSYSTEM_PRESETS).length}`);
  console.log(`Escape-time presets: ${Object.keys(ESCAPE_TIME_PRESETS).length}`);
  console.log(`Newton presets: ${Object.keys(NEWTON_PRESETS).length}`);
  console.log(`Attractor presets: ${Object.keys(ATTRACTOR_PRESETS).length}`);
  console.log(`Inversion presets: ${Object.keys(INVERSION_PRESETS).length}`);
}

main().catch((error) => {
  console.error(error.message || error);
  process.exitCode = 1;
});
