#!/usr/bin/env node
import assert from 'node:assert/strict';
import { resolveApiBaseUrl } from './test-api-v1-base.mjs';

const nodeProcess = globalThis.process;
const log = globalThis.console;
const fetchFn = globalThis.fetch;

function isPng(buffer) {
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  return signature.every((byte, index) => buffer[index] === byte);
}

async function main() {
  const baseUrl = await resolveApiBaseUrl();
  const endpoint = `${baseUrl}/api/v1/escape-time/multibrot?width=128&height=72&backgroundColor=white&mainColorScheme=acu`;
  const response = await fetchFn(endpoint);
  assert.equal(response.status, 200, `Expected 200 from ${endpoint}, got ${response.status}`);
  assert.equal(response.headers.get('content-type'), 'image/png');

  const payload = new Uint8Array(await response.arrayBuffer());
  assert.ok(payload.length > 100, 'PNG payload should not be empty');
  assert.ok(isPng(payload), 'Payload is not a valid PNG stream');

  log.log('quick api v1 test passed');
}

main().catch((error) => {
  log.error(error);
  nodeProcess?.exit(1);
});
