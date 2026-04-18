# Interaction Guidelines Policy

## Purpose

Navigation through PDF content must feel natural and forgiving. Controls must be discoverable, predictable, and paired with clear feedback.

## Tooltips

Every interactive control must have a tooltip:

- Use the `title` attribute as a baseline.
- For richer tooltips (with keyboard shortcut hints), use a `<Tooltip>` component that renders a `role="tooltip"` element associated via `aria-describedby`.
- Tooltip text format for controls with shortcuts: `"Next page (→)"`, `"Zoom in (+)"`.
- Tooltips must appear within 300 ms of hover/focus and must not obscure the control that triggered them.

## Page navigation

- Show current page and total pages at all times: `Page 3 of 42`.
- Previous/Next buttons must be disabled (not hidden) on the first and last pages respectively, with an `aria-disabled="true"` attribute.
- The page number input must accept free-text entry; on `Enter` or blur, clamp the value to `[1, totalPages]` and navigate.
- When navigating, show a loading indicator if the new page takes > 200 ms to render.

## Zoom

- Supported zoom levels: 50%, 75%, 100%, 125%, 150%, 200%, fit-width.
- Zoom changes must be reflected immediately in the UI (optimistic update) and persisted via cookie.
- The zoom control must display the current zoom level as a label (e.g., "125%").

## Sidebar

- On desktop, the sidebar is open by default.
- On mobile, the sidebar is hidden by default and toggled by a hamburger button in the toolbar.
- The sidebar overlay on mobile must be dismissible by tapping outside it or pressing `Escape`.
- The sidebar must show the active booklet highlighted.

## Feedback and status messages

- **Loading:** Show a spinner with descriptive text (`aria-label="Loading PDF"`) while PDF data is being fetched.
- **Success:** No intrusive message — the content appearing is the confirmation.
- **Error:** See [error-handling.md](error-handling.md) for the full error handling policy.
- **Retry in progress:** Show "Retrying… (attempt 2 of 3)" during auto-retry.

## Empty and edge states

- If a booklet has no pages, show: "This booklet appears to be empty. Try downloading it directly."
- If the outline (table of contents) is empty, hide the outline tab — do not show an empty list.

## Validation checklist

- [ ] All controls have tooltips with shortcut hints where applicable
- [ ] Disabled controls use `aria-disabled`, not `display:none`
- [ ] Page input clamps out-of-range values
- [ ] Sidebar dismisses on outside tap on mobile
- [ ] Loading spinner has accessible label
