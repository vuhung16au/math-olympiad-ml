# Responsiveness Policy

## Purpose

HSC Math Hub serves both desktop and mobile users. All code produced by agents must work correctly across every supported viewport without requiring separate code paths.

## Supported breakpoints (Tailwind defaults)

| Name | Min width | Typical device |
|---|---|---|
| `sm` | 640 px | Large phone (landscape) |
| `md` | 768 px | Tablet |
| `lg` | 1024 px | Small laptop |
| `xl` | 1280 px | Desktop |

The sidebar collapses below `md` (see `--sidebar-width` in `styles/variables.css`).

## Rules for agents

- **Write mobile-first CSS.** Base styles target narrow screens; use `md:`, `lg:`, `xl:` modifiers to enhance for wider viewports.
- **Never hard-code pixel widths** for layout containers. Use `w-full`, `max-w-*`, or the `--sidebar-width` variable.
- **Test every new UI at 375 px, 768 px, and 1280 px** before marking work done.
- **Touch targets must be ≥ 44 × 44 px** on all breakpoints (WCAG 2.5.5).
- **The PDF canvas must scale to fit the viewport width** on mobile. Do not clip or overflow horizontally.
- **The toolbar must never overflow off-screen.** On narrow viewports, secondary controls may be hidden behind a menu icon.

## Existing responsive components

- `components/layout/` — shell with collapsible sidebar and mobile menu
- `components/pages/PDFViewer.tsx` — viewer with fit-width mode
- `tests/e2e/responsive.spec.ts` — viewports: 375×812, 768×1024, 1280×800

## Validation checklist

- [ ] Layout does not overflow horizontally at 375 px
- [ ] All interactive controls are reachable and large enough to tap on mobile
- [ ] Sidebar collapses correctly below `md`
- [ ] PDF canvas fits the screen width on mobile
- [ ] Responsive test suite passes (`make test`)
