import { execSync } from 'node:child_process';

const fetchFn = globalThis.fetch;
const nodeProcess = globalThis.process;

function buildCandidateUrlsFromListeners() {
  try {
    const output = execSync('lsof -n -P -iTCP -sTCP:LISTEN', { encoding: 'utf8' });
    const ports = extractPorts(output);
    return [...ports]
      .sort((a, b) => a - b)
      .map((port) => `http://127.0.0.1:${port}`);
  } catch {
    return [];
  }
}

function extractPorts(output) {
  const ports = new Set();
  for (const line of output.split('\n')) {
    const port = parsePortFromLine(line);
    if (port !== null) ports.add(port);
  }
  return ports;
}

function parsePortFromLine(line) {
  if (!line || !line.includes('LISTEN')) return null;
  const match = line.match(/:(\d+)\s+\(LISTEN\)/);
  if (!match) return null;
  const port = Number.parseInt(match[1], 10);
  if (!Number.isFinite(port) || port < 1 || port > 65535) return null;
  return port;
}

async function isFractalsApi(baseUrl) {
  try {
    const response = await fetchFn(`${baseUrl}/api/presets`);
    if (!response.ok) return false;
    const payload = await response.json();
    return Boolean(payload?.presets);
  } catch {
    return false;
  }
}

export async function resolveApiBaseUrl() {
  const envUrl = nodeProcess?.env?.FRACTALS_API_BASE;
  if (envUrl) return envUrl;

  const candidates = buildCandidateUrlsFromListeners();
  for (const baseUrl of candidates) {
    // Prefer real app endpoints, not just open ports.
    // eslint-disable-next-line no-await-in-loop
    if (await isFractalsApi(baseUrl)) return baseUrl;
  }

  throw new Error(
    'Cannot auto-detect a running fractals API server. Start `npm run dev` and retry, or set FRACTALS_API_BASE.',
  );
}
