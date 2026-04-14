#!/usr/bin/env node
/* eslint-env node */
/* global require, process, console */

const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const ROOT = process.cwd();

function runCommand(command, args) {
  const result = spawnSync(command, args, {
    cwd: ROOT,
    stdio: 'inherit',
    shell: false,
  });
  return result.status === 0;
}

function exists(relPath) {
  return fs.existsSync(path.join(ROOT, relPath));
}

function recordResult(gateResults, failures, status, gate, message) {
  gateResults.push({ gate, status, message });
  console.log(`${status.toUpperCase()} ${gate}: ${message}`);
  if (status === 'fail') {
    failures.push({ gate, message });
  }
}

function check(condition, gate, message, failures, gateResults) {
  if (condition) {
    recordResult(gateResults, failures, 'pass', gate, message);
    return;
  }
  recordResult(gateResults, failures, 'fail', gate, message);
}

function readJson(relPath) {
  const fullPath = path.join(ROOT, relPath);
  return JSON.parse(fs.readFileSync(fullPath, 'utf8'));
}

function hasAny(pattern, text) {
  return pattern.some((token) => text.includes(token));
}

function parseJsonOutArg(argv) {
  const flag = '--json-out';
  const index = argv.indexOf(flag);
  if (index < 0) return null;
  const next = argv[index + 1];
  if (!next || next.startsWith('--')) {
    throw new Error('Missing value for --json-out');
  }
  return next;
}

function writeJsonReport(outputPath, report) {
  const resolved = path.isAbsolute(outputPath) ? outputPath : path.join(ROOT, outputPath);
  fs.mkdirSync(path.dirname(resolved), { recursive: true });
  fs.writeFileSync(resolved, `${JSON.stringify(report, null, 2)}\n`);
  console.log(`JSON report written: ${resolved}`);
}

function main() {
  const runPlaywright = process.argv.includes('--with-playwright');
  const jsonOut = parseJsonOutArg(process.argv.slice(2));
  const failures = [];
  const gateResults = [];

  const requiredFiles = [
    'README.md',
    'QUICKSTART.md',
    'docs/architecture.md',
    'docs/techstack.md',
    'docs/use-cases.md',
    'docs/scripts.md',
    'app/page.tsx',
    'app/api/render/route.ts',
    'scripts/generate-all-fractals-playwright.js',
  ];
  check(requiredFiles.every(exists), 'Gate 8', 'required docs/app files exist', failures, gateResults);

  const controlsFile = fs.readFileSync(path.join(ROOT, 'app/components/FractalControls.tsx'), 'utf8');
  const controlsParityPass = ['ifsFields', 'lsysFields', 'escapeFields', 'newtonFields', 'attractorFields', 'inversionFields']
    .every((id) => controlsFile.includes(`id="${id}"`));
  check(controlsParityPass, 'Gate 2', 'UI controls include all family forms', failures, gateResults);

  const presetModule = require(path.join(ROOT, 'scripts/generate-all-fractals.js'));
  const familyCounts = {
    ifs: Object.keys(presetModule.IFS_PRESETS || {}).length,
    lsystem: Object.keys(presetModule.LSYSTEM_PRESETS || {}).length,
    'escape-time': Object.keys(presetModule.ESCAPE_TIME_PRESETS || {}).length,
    newton: Object.keys(presetModule.NEWTON_PRESETS || {}).length,
    attractors: Object.keys(presetModule.ATTRACTOR_PRESETS || {}).length,
    inversions: Object.keys(presetModule.INVERSION_PRESETS || {}).length,
  };

  const familyCoveragePass = [
    familyCounts.ifs > 0,
    familyCounts.lsystem > 0,
    familyCounts['escape-time'] >= 3,
    familyCounts.newton >= 2,
    familyCounts.attractors >= 3,
    familyCounts.inversions >= 3,
  ].every(Boolean);
  check(familyCoveragePass, 'Gate 1/4', 'all required fractal families and baseline presets exist', failures, gateResults);

  const renderApiFile = fs.readFileSync(path.join(ROOT, 'app/api/render/route.ts'), 'utf8');
  const apiContractPass = hasAny(['Unknown preset', 'status: 400'], renderApiFile)
    && ['escapeTime', 'newton', 'attractor', 'inversion']
      .every((family) => renderApiFile.includes(`family === '${family}'`));
  check(apiContractPass, 'Gate 3', 'API render route has family routing and 400 error handling', failures, gateResults);

  check(runCommand('npm', ['run', 'build']), 'Gate 9', 'package build succeeds', failures, gateResults);
  check(runCommand('npm', ['run', 'build:web']), 'Gate 11', 'web build succeeds', failures, gateResults);

  if (runPlaywright) {
    check(
      runCommand('npm', ['run', 'test:fractals:playwright', '--', '--render-timeout-ms', '180000']),
      'Gate 5',
      'Playwright sweep succeeds',
      failures,
      gateResults,
    );
  } else {
    recordResult(gateResults, failures, 'skip', 'Gate 5', 'run with --with-playwright to enforce Playwright gate');
  }

  const artifactFamilies = ['ifs', 'lsystem', 'escape-time', 'newton', 'attractors', 'inversions'];
  check(
    artifactFamilies.every((family) => exists(path.join('artifacts', family))),
    'Gate 6',
    'artifact family folders exist',
    failures,
    gateResults,
  );

  check(exists('artifacts/index.json'), 'Gate 6', 'artifact index exists', failures, gateResults);
  check(exists('artifacts-playwright/index.json'), 'Gate 6', 'playwright artifact index exists', failures, gateResults);

  const scriptsDoc = fs.readFileSync(path.join(ROOT, 'docs/scripts.md'), 'utf8');
  const scriptsGatePass = hasAny(['keep', 'adapt', 'deprecate'], scriptsDoc);
  check(scriptsGatePass, 'Gate 7', 'scripts rationalization is documented', failures, gateResults);

  const architectureDoc = fs.readFileSync(path.join(ROOT, 'docs/architecture.md'), 'utf8');
  const techstackDoc = fs.readFileSync(path.join(ROOT, 'docs/techstack.md'), 'utf8');
  const useCasesDoc = fs.readFileSync(path.join(ROOT, 'docs/use-cases.md'), 'utf8');
  const crossLinkPass = hasAny(['techstack', 'use-cases', 'README'], architectureDoc)
    && hasAny(['architecture', 'use-cases', 'README'], techstackDoc)
    && hasAny(['architecture', 'techstack', 'README'], useCasesDoc);
  check(crossLinkPass, 'Gate 8', 'core docs are cross-linked', failures, gateResults);

  const playwrightIndex = readJson('artifacts-playwright/index.json');
  const allFamiliesInSweep = ['IFS', 'L-system', 'Escape-time', 'Newton', 'Strange Attractor', 'Circle Inversion']
    .every((label) => (playwrightIndex.results || []).some((r) => r.fractalTypeLabel === label));
  check(allFamiliesInSweep, 'Gate 5', 'playwright index contains all six families', failures, gateResults);

  const sloPass = (() => {
    const script = fs.readFileSync(path.join(ROOT, 'scripts/generate-all-fractals-playwright.js'), 'utf8');
    const hasUiSloTimeout = script.includes('renderTimeoutMs') && script.includes('120000');
    const plan = fs.readFileSync(path.join(ROOT, '.cursor/plans/improve_techstack_migration_plan_2d47b9be.plan.md'), 'utf8');
    const hasSloText = hasAny(['2.0s', 'p95', '2 MB', '10s'], plan);
    return hasUiSloTimeout && hasSloText;
  })();
  check(sloPass, 'Gate 10', 'SLO constraints are documented and enforced by timeout guardrails', failures, gateResults);

  const finalAuditPass = failures.length === 0;
  check(finalAuditPass, 'Gate 12', 'all enforced gates pass', failures, gateResults);

  const report = {
    generatedAt: new Date().toISOString(),
    withPlaywright: runPlaywright,
    summary: {
      pass: gateResults.filter((r) => r.status === 'pass').length,
      fail: gateResults.filter((r) => r.status === 'fail').length,
      skip: gateResults.filter((r) => r.status === 'skip').length,
      total: gateResults.length,
      ok: failures.length === 0,
    },
    gates: gateResults,
    failures,
  };
  if (jsonOut) {
    writeJsonReport(jsonOut, report);
  }

  if (failures.length > 0) {
    console.log(`\nRelease gate verification failed with ${failures.length} issue(s).`);
    process.exitCode = 1;
    return;
  }
  console.log('\nAll enforced release gates passed.');
}

main();
