# Cookies & localStorage Policy

## Purpose

HSC Math Hub uses browser storage only to improve the user experience across sessions. No personally identifiable information (PII) is ever stored.

## Permitted data

Agents may only read/write the following keys:

| Key | Storage | Type | Expiry | Purpose |
|---|---|---|---|---|
| `last-url` | Cookie | `string` (path e.g. `/booklets/hsc-sequences`) | 30 days | Restore the last opened booklet on next visit |
| `last-page-{slug}` | Cookie | `number` (page index) | 30 days | Restore the last viewed page within a booklet |
| `zoom-level` | Cookie | `string` (e.g. `"fit-width"`, `"125%"`) | 30 days | Persist zoom preference |
| `theme` | Cookie | `"light"` \| `"dark"` \| `"sepia"` | 365 days | Persist theme preference |
| `shortcuts-seen` | Cookie | `"1"` | 365 days | Suppress first-visit shortcut hint after dismissal |
| `session-state` | `sessionStorage` | JSON object | Session (tab close) | Transient viewer state (scroll position, outline open/closed) |

## Rules for agents

1. **No PII.** Never store names, email addresses, authentication tokens, or any data that identifies a real person.
2. **SameSite and Secure attributes** must be set on all cookies:
   ```
   Set-Cookie: last-url=...; SameSite=Lax; Secure; Path=/; Max-Age=2592000
   ```
3. **Do not create new cookie keys** without adding them to the table above and updating this document.
4. **Cookie values must be validated** on read before use — treat them as untrusted input (a user may have manually edited them). Always clamp numeric values to valid ranges (e.g., page number within `[1, totalPages]`).
5. **`sessionStorage` only for transient state.** Do not persist data that should survive page reloads to `sessionStorage`.
6. **Consent.** These cookies are strictly functional (no tracking, no analytics). They do not require a consent banner under ePrivacy Directive exemptions. Do not add tracking or advertising cookies without a separate privacy review.

## Cookie helper location

Cookie read/write logic lives in `lib/cookies.ts` (or equivalent). Agents must use these helpers rather than manipulating `document.cookie` directly. This keeps all cookie names centralized and prevents typos.

## Testing

- `tests/e2e/restore-last-session.spec.ts` — verifies `last-url` cookie restore behavior.
- `tests/e2e/toolbar-and-zoom.spec.ts` — verifies zoom cookie persistence.
- Any new cookie behavior added by agents must have a corresponding e2e test.
