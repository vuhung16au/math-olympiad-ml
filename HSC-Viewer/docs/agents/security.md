# Security Policy

## Purpose

HSC Math Hub renders third-party PDF content in the browser. Agents must not introduce code that exposes users to XSS, clickjacking, or other injection attacks.

## XSS in PDF rendering

- **Never inject PDF text content into the DOM as raw HTML.** All text extracted from PDFs must be treated as untrusted data and rendered as plain text nodes or via React's JSX (which escapes by default).
- **Never use `dangerouslySetInnerHTML`** with data derived from PDF content, URL parameters, cookie values, or any external source.
- If annotations or links from within the PDF are rendered, sanitize all `href` values before use (see URL validation below).

## iframe sandboxing

Any `<iframe>` element used in the viewer must carry a restrictive `sandbox` attribute:

```html
<iframe
  sandbox="allow-scripts allow-same-origin"
  src="..."
/>
```

Do not add `allow-forms`, `allow-popups`, or `allow-top-navigation` unless there is an explicit, reviewed reason.

## Content Security Policy (CSP)

The application must serve the following CSP headers (configure in `next.config.ts` via `headers()`):

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: blob: raw.githubusercontent.com;
  connect-src 'self' raw.githubusercontent.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
```

- `unsafe-inline` for scripts/styles is required by Next.js runtime; do not widen it further.
- Do not add `unsafe-eval` — it is not required and significantly widens the attack surface.
- Extend `connect-src` and `img-src` only via explicit, reviewed additions to `next.config.ts`.

## User-supplied URL validation

Any URL provided by the user (e.g., via query parameters, route segments, or form input) must be validated before use:

```ts
import { URL } from 'url';

function isSafeBookletUrl(raw: string): boolean {
  try {
    const parsed = new URL(raw);
    return (
      (parsed.protocol === 'https:') &&
      parsed.hostname === 'raw.githubusercontent.com'
    );
  } catch {
    return false;
  }
}
```

- Only `https://raw.githubusercontent.com` URLs are permitted as PDF sources.
- Reject and do not fetch any URL that fails this check. Show the user a generic error — do not echo the invalid URL back in an error message (prevents reflected XSS).

## Dependency hygiene

- Do not add new dependencies that have known critical CVEs.
- Run `bun audit` before submitting changes that add or update packages.

## Secrets

- Never commit API keys, tokens, or credentials.
- Never log cookie values or query parameters that could contain sensitive data.
