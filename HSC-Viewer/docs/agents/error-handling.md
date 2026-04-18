# Error Handling Policy

## Purpose

When something goes wrong, users should never see a blank page, a JavaScript stack trace, or a broken layout. All error states must be graceful, informative, and where possible, self-recovering.

## PDF load failure

### Behavior

1. On initial load failure, **retry automatically up to 3 times** with exponential back-off (500 ms, 1 s, 2 s).
2. During retries, show: `"Loading… (attempt 2 of 3)"` in place of the PDF canvas.
3. After 3 failed attempts, show the error state UI (see below).

### Error state UI

```
┌─────────────────────────────────────────────┐
│  ⚠  Could not load this booklet             │
│                                             │
│  We weren't able to load the PDF after      │
│  several attempts. This may be a temporary  │
│  network issue.                             │
│                                             │
│  [Try again]   [Download PDF]               │
└─────────────────────────────────────────────┘
```

- "Try again" resets the retry counter and starts the fetch again.
- "Download PDF" opens the raw PDF URL in a new tab.
- The error container must use `role="alert"` so screen readers announce it.

## Missing page

When `react-pdf` reports a page number that does not exist in the document:

- Show: `"Page [N] is not available in this booklet."` inside the PDF canvas area.
- Do not navigate away or reload. Let the user use the navigation controls to go to a valid page.

## Network offline

Detect `navigator.onLine` and the `offline` event:

- When the user goes offline, show a dismissible banner: `"You're offline. Previously viewed pages are still available."` (relies on service worker cache — see [offline-caching.md](offline-caching.md)).
- When the user comes back online, dismiss the banner automatically.

## JavaScript errors (ErrorBoundary)

`components/ui/ErrorBoundary.tsx` wraps the viewer. When it catches an unhandled error:

- Log the error to the console (and optionally to an error tracking service).
- Show a friendly message: `"Something went wrong. Please refresh the page."` with a "Refresh" button.
- Never expose raw error messages or stack traces to users.

## Implementation rules

- Never use bare `throw` without a catch boundary in async PDF loading code.
- Always handle `Promise` rejections — never leave unhandled rejections in PDF fetch or render code.
- All user-facing error strings must be defined as constants in a single location (e.g., `lib/errors.ts`) to make them easy to update.
- Error UI must match the color palette in [colors.md](colors.md) and be readable in all three theme modes.

## Testing

Existing coverage in `tests/e2e/error-and-recovery.spec.ts`. New error paths added by agents must have corresponding Playwright test cases.
