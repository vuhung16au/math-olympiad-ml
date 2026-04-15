#!/usr/bin/env node

import assert from 'node:assert/strict';
import { resolveApiBaseUrl } from './test-api-v1-base.mjs';

const nodeProcess = globalThis.process;
const log = globalThis.console;
const fetchFn = globalThis.fetch;

const familyToSlug = {
  ifs: 'ifs',
  lsystem: 'lsystem',
  escapeTime: 'escape-time',
  newton: 'newton',
  attractor: 'strange-attractor',
  inversion: 'circle-inversion',
};

function isPng(buffer) {
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  return signature.every((byte, index) => buffer[index] === byte);
}

async function fetchPng(url) {
  const response = await fetchFn(url);
  assert.equal(response.status, 200, `Expected 200 from ${url}, got ${response.status}`);
  assert.equal(response.headers.get('content-type'), 'image/png');
  const bytes = new Uint8Array(await response.arrayBuffer());
  assert.ok(bytes.length > 100, `PNG payload too small for ${url}`);
  assert.ok(isPng(bytes), `Invalid PNG for ${url}`);
}

async function main() {
  const baseUrl = await resolveApiBaseUrl();
  const presetsResponse = await fetchFn(`${baseUrl}/api/presets`);
  assert.equal(presetsResponse.status, 200, 'Cannot fetch /api/presets');
  const payload = await presetsResponse.json();
  const presets = payload?.presets ?? {};

  for (const [family, slug] of Object.entries(familyToSlug)) {
    const firstPreset = Object.keys(presets[family] ?? {})[0];
    assert.ok(firstPreset, `No preset found for family ${family}`);
    const url = `${baseUrl}/api/v1/${slug}/${firstPreset}?width=128&height=72&mainColorScheme=acu&backgroundColor=white`;
    await fetchPng(url);
    log.log(`checked ${family}/${firstPreset}`);
  }

  log.log('full api v1 family test passed');
}

main().catch((error) => {
  log.error(error);
  nodeProcess?.exit(1);
});
