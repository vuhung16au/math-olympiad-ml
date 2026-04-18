# Mobile-First Policy

## Purpose

Mobile users are the primary audience. Every design and implementation decision must first satisfy the mobile experience, then be enhanced for desktop.

## Principles

1. **Design for touch first.** Assume fat fingers, not a precise cursor.
2. **Minimize load weight.** Mobile users may be on 4G or slower. See [performance.md](performance.md) for budgets.
3. **Prefer native scroll over custom scroll containers** where possible — native scroll is faster and more accessible on mobile.
4. **Avoid hover-only interactions.** Any feature accessible only on hover must have an equivalent tap interaction.
5. **Reduce cognitive load.** Show only essential controls on narrow screens; reveal secondary controls progressively.

## PDF viewer on mobile

- Default zoom mode is **fit-width**, not a fixed percentage.
- Page navigation (previous/next) must be reachable with a single thumb tap while holding the phone in one hand.
- The toolbar should collapse secondary controls (e.g., print, fullscreen) into an overflow menu on viewports < 640 px.
- Pinch-to-zoom on the PDF canvas must not conflict with browser zoom.

## Performance on mobile

Target metrics on a mid-range Android device on a simulated 4G connection:

| Metric | Target |
|---|---|
| First Contentful Paint | ≤ 1.5 s |
| Time to Interactive | ≤ 3 s |
| PDF first page render | ≤ 500 ms after PDF data available |

See [performance.md](performance.md) for full details.

## Testing

- Playwright viewport `375×812` (iPhone 14 logical resolution) is the canonical mobile test viewport.
- Use `tests/e2e/responsive.spec.ts` to validate mobile behavior.
- When adding new UI, add a mobile assertion to the responsive spec.
