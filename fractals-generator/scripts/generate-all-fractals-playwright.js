#!/usr/bin/env node
/* eslint-env node */
/* global require, process, console */

const fs = require('node:fs/promises');
const path = require('node:path');
const { spawn } = require('node:child_process');

const DEFAULT_BASE_URL = 'http://127.0.0.1:3000';
const DEFAULT_OUT_DIR = path.resolve(process.cwd(), 'artifacts-playwright');

function printHelp() {
  console.log([
    'Generate screenshots and smoke tests for Next.js fractal presets.',
    '',
    'Usage:',
    '  node scripts/generate-all-fractals-playwright.js [--url <url>] [--out <dir>] [--headless <true|false>]',
    '',
    'Examples:',
    '  node scripts/generate-all-fractals-playwright.js',
    '  node scripts/generate-all-fractals-playwright.js --headless false',
    '  node scripts/generate-all-fractals-playwright.js --out artifacts-playwright/custom',
  ].join('\n'));
}

function parseArgs(argv) {
  const options = {
    url: DEFAULT_BASE_URL,
    outDir: DEFAULT_OUT_DIR,
    headless: true,
    renderTimeoutMs: 120000,
    noServer: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') {
      options.help = true;
      return options;
    }
    if (arg === '--url') {
      options.url = String(argv[i + 1] ?? '');
      i += 1;
      continue;
    }
    if (arg === '--out') {
      options.outDir = path.resolve(process.cwd(), String(argv[i + 1] ?? ''));
      i += 1;
      continue;
    }
    if (arg === '--headless') {
      const value = String(argv[i + 1] ?? 'true').toLowerCase();
      options.headless = value !== 'false';
      i += 1;
      continue;
    }
    if (arg === '--render-timeout-ms') {
      options.renderTimeoutMs = Number(argv[i + 1] ?? '120000');
      i += 1;
      continue;
    }
    if (arg === '--no-server') {
      options.noServer = true;
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }

  return options;
}

function slugify(input) {
  return String(input)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

function spawnServer() {
  const child = spawn('npm', ['run', 'start', '--', '--hostname', '127.0.0.1', '--port', '3000'], {
    cwd: process.cwd(),
    shell: false,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return child;
}

async function waitForUrl(page, url, retries = 20) {
  let lastError = null;
  for (let i = 0; i < retries; i += 1) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 5000 });
      await page.locator('#fractalType').waitFor({ state: 'visible', timeout: 15000 });
      return;
    } catch (error) {
      lastError = error;
      await page.waitForTimeout(600);
    }
  }
  throw new Error(`Cannot reach ${url}: ${String(lastError?.message || lastError)}`);
}

async function selectOptionAndWait(selectLocator, value) {
  await selectLocator.selectOption(value);
  await selectLocator.evaluate((el) => el.dispatchEvent(new globalThis.Event('change', { bubbles: true })));
}

async function waitRenderSettled(page, timeoutMs) {
  const meta = page.locator('#meta');
  await meta.waitFor({ state: 'visible', timeout: timeoutMs });
  await page.waitForTimeout(250);
  await page.waitForFunction(() => {
    const el = globalThis.document.querySelector('#meta');
    if (!el) return false;
    const text = (el.textContent || '').toLowerCase();
    return text.includes('rendered') || text.includes('failed');
  }, { timeout: timeoutMs });
}

async function getMetaText(page) {
  return page.locator('#meta').innerText();
}

async function canvasHasInk(page) {
  return page.$eval('#canvas', (canvas) => {
    const ctx = canvas.getContext('2d');
    if (!ctx) return false;
    const { width, height } = canvas;
    const image = ctx.getImageData(0, 0, width, height).data;
    let nonWhite = 0;
    const stride = 4 * 6;
    for (let i = 0; i < image.length; i += stride) {
      const r = image[i];
      const g = image[i + 1];
      const b = image[i + 2];
      if (!(r > 246 && g > 246 && b > 246)) {
        nonWhite += 1;
      }
      if (nonWhite > 12) return true;
    }
    return false;
  });
}

function clampNumber(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

async function parameterTrials(page, fractalType) {
  const trials = [];
  if (fractalType === 'ifs') {
    const iterations = page.locator('#ifsIterations');
    const density = page.locator('#ifsDensity');
    const currentIterations = Number(await iterations.inputValue());
    const currentDensity = Number(await density.inputValue());
    trials.push(
      async () => {
        await iterations.fill(String(clampNumber(Math.round(currentIterations * 0.8), 1000, 600000)));
        await density.fill(String(clampNumber(Math.round(currentDensity * 0.9), 1, 150)));
      },
      async () => {
        await iterations.fill(String(clampNumber(Math.round(currentIterations * 1.15), 1000, 600000)));
        await density.fill(String(clampNumber(Math.round(currentDensity * 1.1), 1, 150)));
      },
    );
  } else if (fractalType === 'lsystem') {
    const iterations = page.locator('#lsIterations');
    const distance = page.locator('#lsDistance');
    const currentIterations = Number(await iterations.inputValue());
    const currentDistance = Number(await distance.inputValue());
    trials.push(
      async () => {
        await iterations.fill(String(clampNumber(Math.round(currentIterations * 0.8), 0, 13)));
        await distance.fill(String(clampNumber(Number((currentDistance * 0.9).toFixed(2)), 0.1, 40)));
      },
      async () => {
        await iterations.fill(String(clampNumber(Math.round(currentIterations + 1), 0, 13)));
        await distance.fill(String(clampNumber(Number((currentDistance * 1.05).toFixed(2)), 0.1, 40)));
      },
    );
  } else if (fractalType === 'escapeTime') {
    const maxIterations = page.locator('#etMaxIterations');
    const power = page.locator('#etPower');
    const currentIterations = Number(await maxIterations.inputValue());
    const currentPower = Number(await power.inputValue());
    trials.push(
      async () => {
        await maxIterations.fill(String(clampNumber(Math.round(currentIterations * 0.8), 20, 4000)));
      },
      async () => {
        await maxIterations.fill(String(clampNumber(Math.round(currentIterations * 1.25), 20, 4000)));
        await power.fill(String(clampNumber(Math.round(currentPower), 2, 8)));
      },
    );
  } else if (fractalType === 'newton') {
    const maxIterations = page.locator('#ntMaxIterations');
    const epsilon = page.locator('#ntEpsilon');
    const currentIterations = Number(await maxIterations.inputValue());
    const currentEpsilon = Number(await epsilon.inputValue());
    trials.push(
      async () => {
        await maxIterations.fill(String(clampNumber(Math.round(currentIterations * 0.85), 5, 200)));
      },
      async () => {
        await epsilon.fill(String(clampNumber(currentEpsilon * 1.5, 0.00000001, 0.1)));
      },
    );
  } else if (fractalType === 'attractor') {
    const iterations = page.locator('#atIterations');
    const a = page.locator('#atA');
    const currentIterations = Number(await iterations.inputValue());
    const currentA = Number(await a.inputValue());
    trials.push(
      async () => {
        await iterations.fill(String(clampNumber(Math.round(currentIterations * 0.75), 10000, 2000000)));
      },
      async () => {
        await a.fill(String(clampNumber(Number((currentA + 0.05).toFixed(4)), -5, 5)));
      },
    );
  } else if (fractalType === 'inversion') {
    const depth = page.locator('#ivDepth');
    const minRadius = page.locator('#ivMinRadius');
    const currentDepth = Number(await depth.inputValue());
    const currentMinRadius = Number(await minRadius.inputValue());
    trials.push(
      async () => {
        await depth.fill(String(clampNumber(currentDepth + 1, 1, 12)));
      },
      async () => {
        await minRadius.fill(String(clampNumber(Number((currentMinRadius * 1.5).toFixed(4)), 0.0001, 0.2)));
      },
    );
  }
  return trials.slice(0, 2);
}

async function runPresetTests(page, outDir, fractalType, fractalTypeLabel, presetValue, presetLabel, renderTimeoutMs) {
  const generateBtn = page.locator('#generateBtn');
  const resetBtn = page.locator('#resetBtn');

  await resetBtn.click({ timeout: 15000 });
  await generateBtn.click({ timeout: 15000 });
  await waitRenderSettled(page, renderTimeoutMs);
  const metaDefault = await getMetaText(page);
  const hasInkDefault = await canvasHasInk(page);
  if (!hasInkDefault || /failed/i.test(metaDefault)) {
    throw new Error(`Default render failed for ${fractalTypeLabel} / ${presetLabel}: ${metaDefault}`);
  }

  const presetSlug = slugify(presetLabel);
  const typeSlug = slugify(fractalTypeLabel);
  const screenshotPath = path.join(outDir, typeSlug, `${presetSlug}.png`);
  await fs.mkdir(path.dirname(screenshotPath), { recursive: true });
  await page.screenshot({ path: screenshotPath, fullPage: true });

  const trials = await parameterTrials(page, fractalType);
  const trialResults = [];
  for (let i = 0; i < trials.length; i += 1) {
    await resetBtn.click();
    await trials[i]();
    await generateBtn.click();
    await waitRenderSettled(page, renderTimeoutMs);
    const meta = await getMetaText(page);
    if (/failed/i.test(meta)) {
      throw new Error(`Parameter trial ${i + 1} failed for ${fractalTypeLabel} / ${presetLabel}: ${meta}`);
    }
    trialResults.push({ trial: i + 1, meta });
  }

  return {
    fractalType,
    fractalTypeLabel,
    presetValue,
    presetLabel,
    screenshot: path.relative(outDir, screenshotPath),
    defaultMeta: metaDefault,
    trials: trialResults,
  };
}

async function generateAll(options) {
  console.log('Starting Playwright sweep...');
  const { chromium } = await import('playwright');
  console.log('Launching Chromium...');
  const browser = await chromium.launch({ headless: options.headless });
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  console.log('Browser launched.');
  const server = options.noServer ? null : spawnServer();
  const serverLog = [];

  if (server) {
    server.stdout.on('data', (chunk) => {
      serverLog.push(String(chunk));
    });
    server.stderr.on('data', (chunk) => {
      serverLog.push(String(chunk));
    });
  }

  try {
    console.log(`Opening URL: ${options.url}`);
    await waitForUrl(page, options.url, 60);
    console.log('Page ready. Discovering fractal options...');

    const fractalTypeSelect = page.locator('#fractalType');
    const presetSelect = page.locator('#preset');
    const typeOptions = await fractalTypeSelect.locator('option').evaluateAll((nodes) => nodes.map((n) => ({
      value: n.value,
      label: n.textContent || n.value,
    })));

    const summary = {
      generatedAt: new Date().toISOString(),
      url: options.url,
      outDir: options.outDir,
      totalTypes: 0,
      totalPresets: 0,
      totalTrials: 0,
      results: [],
    };

    for (const typeOption of typeOptions) {
      console.log(`Testing fractal type: ${typeOption.label}`);
      await selectOptionAndWait(fractalTypeSelect, typeOption.value);
      await page.waitForTimeout(100);

      const presets = await presetSelect.locator('option').evaluateAll((nodes) => nodes.map((n) => ({
        value: n.value,
        label: n.textContent || n.value,
      })));

      summary.totalTypes += 1;

      for (const preset of presets) {
        console.log(`Running preset: ${typeOption.label} / ${preset.label}`);
        await selectOptionAndWait(presetSelect, preset.value);
        const result = await runPresetTests(
          page,
          options.outDir,
          typeOption.value,
          typeOption.label,
          preset.value,
          preset.label,
          options.renderTimeoutMs,
        );
        summary.results.push(result);
        summary.totalPresets += 1;
        summary.totalTrials += result.trials.length;
        console.log(`PASS: ${typeOption.label} / ${preset.label}`);
      }
    }

    await fs.mkdir(options.outDir, { recursive: true });
    await fs.writeFile(path.join(options.outDir, 'index.json'), `${JSON.stringify(summary, null, 2)}\n`);
    console.log('Done.');
    console.log(`Artifacts directory: ${options.outDir}`);
    console.log(`Checked ${summary.totalTypes} types, ${summary.totalPresets} presets, ${summary.totalTrials} parameter trials.`);
  } finally {
    if (server && !server.killed) {
      server.kill('SIGTERM');
    }
    await browser.close();
    if (serverLog.length > 0) {
      await fs.mkdir(options.outDir, { recursive: true });
      await fs.writeFile(path.join(options.outDir, 'server.log'), serverLog.join(''));
    }
  }
}

async function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      printHelp();
      return;
    }
    await generateAll(options);
  } catch (error) {
    console.error(error.message || error);
    process.exitCode = 1;
  }
}

main();
