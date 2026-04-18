# Analytics Policy

## Purpose

HSC-Viewer uses Vercel Analytics to track reader behaviour. Agents must use the established pattern in `lib/analytics.ts` for all new events. Raw `track()` calls outside that module are not permitted.

## How it works

Vercel Analytics is initialised in `app/layout.tsx` via `<Analytics />` (automatic page views). Custom events are fired by calling wrappers in `lib/analytics.ts`, which call `track()` from `@vercel/analytics`.

## Existing events

| Function | Event name | Properties | When to call |
|---|---|---|---|
| `trackBookletOpened(title)` | `booklet_opened` | `booklet` | User opens a booklet page |
| `trackPdfNavigation(title, page, total)` | `pdf_page_navigation` | `booklet`, `page`, `totalPages` | User navigates to a new page |
| `trackPdfZoom(title, zoomPercent)` | `pdf_zoom` | `booklet`, `zoomPercent` | User changes zoom level |
| `trackPdfAction(title, action)` | `pdf_action` | `booklet`, `action` | Print, download, fullscreen, fit-width |

## Adding a new event

1. **Add a wrapper function in `lib/analytics.ts`** — never call `track()` inline in a component:

   ```ts
   // lib/analytics.ts
   export function trackShortcutUsed(shortcut: string) {
     track('shortcut_used', { shortcut });
   }
   ```

2. **Use descriptive, snake_case event names** that read as past-tense actions: `booklet_opened`, `pdf_zoom`, `shortcut_used`.

3. **Keep property keys short and lowercase.** Vercel Analytics has a property value length limit — do not send unbounded strings (e.g., full URLs or user-entered text).

4. **Never send PII.** Event properties must not include names, email addresses, IP-derived data, or any value that could identify an individual.

5. **Call the wrapper from the component**, not from inside `lib/` utility functions (keeps analytics concerns out of pure logic):

   ```ts
   // components/pages/PDFViewer.tsx  — Good
   trackPdfZoom(booklet.title, newScale * 100);

   // lib/pdf-helpers.ts  — Bad: analytics in pure utilities
   ```

6. **Update the table in this document** when adding a new wrapper.

## What not to track

- Individual keystrokes or text input content
- Cookie values or preferences (theme, zoom level — those are preferences, not events)
- Error details with stack traces or file paths
- Any event fired more than once per user action (e.g., do not fire on every render, only on deliberate user interaction)

## Testing

Vercel Analytics `track()` calls are no-ops in test environments. Playwright tests do not need to assert on analytics. If you need to verify a call occurs, use `jest.spyOn` in a unit test — but given this project has no unit tests, simply ensure the call site is correct via code review.
