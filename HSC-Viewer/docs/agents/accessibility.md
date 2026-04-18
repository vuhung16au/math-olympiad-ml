# Accessibility Policy

## Purpose

HSC Math Hub must be usable by everyone, including users of assistive technology, users who prefer different visual themes, and users who rely on keyboard-only navigation.

## Standard

Target **WCAG 2.1 Level AA** compliance.

## Theme modes

The viewer supports three themes. Agents must ensure all components render correctly in all three:

| Theme | Background | Text | Accent |
|---|---|---|---|
| Light | `--color-white` / `--color-ivory` | `--color-black` / `--color-charcoal` | `--color-purple` |
| Dark | `--color-charcoal` | `--color-ivory` / `--color-white` | `--color-purple` |
| Sepia | `--color-ivory` | `--color-charcoal` | `--color-stone` |

Theme preference is persisted via a cookie (see [cookies.md](cookies.md)).

## Keyboard navigation

All interactive elements must be fully operable by keyboard:

- **Tab / Shift+Tab** — move focus forward/backward through interactive elements in DOM order
- **Enter / Space** — activate buttons and links
- **Arrow keys** — navigate within composite widgets (e.g., page number input, zoom selector)
- **Escape** — close modals, menus, and overlays

Focus order must follow visual reading order. Do not remove focus outlines; style them using `--color-purple` so they are visible on all theme backgrounds.

## ARIA requirements

- All icon-only buttons must have `aria-label` describing their action.
- The PDF canvas container must have `role="document"` and `aria-label` with the booklet title.
- Page navigation region must be wrapped in `<nav aria-label="Page navigation">`.
- Error messages must use `role="alert"` so screen readers announce them immediately.
- Loading states must use `aria-busy="true"` on the relevant container.
- Tooltips must be associated via `aria-describedby`.

## Color contrast

- Normal text: minimum contrast ratio **4.5:1** against background.
- Large text (≥ 18 pt or ≥ 14 pt bold): minimum **3:1**.
- UI components and focus indicators: minimum **3:1**.
- Verify contrast in all three themes using the palette in [colors.md](colors.md).

## Reduced motion

Respect `prefers-reduced-motion`. Wrap all transitions and animations:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Validation checklist

- [ ] All interactive elements are focusable and operable by keyboard
- [ ] No keyboard trap exists anywhere in the UI
- [ ] Focus indicator is visible in all three themes
- [ ] All icon buttons have `aria-label`
- [ ] Error messages use `role="alert"`
- [ ] Contrast ratios pass in light, dark, and sepia modes
- [ ] `prefers-reduced-motion` suppresses animations
