# Colors Policy

## Purpose

All colors in the HSC Math Hub UI must come from the design system defined in `styles/variables.css`. Agents must never introduce arbitrary hex or RGB values outside this file.

## Color palette

These are the only colors agents may use:

### Primary colors

| Variable | Value | Usage |
|---|---|---|
| `--color-purple` | `rgb(60, 16, 83)` | Primary brand color — headers, active states, focus rings |
| `--color-red` | `rgb(242, 18, 12)` | Accent — badges, important highlights |
| `--color-black` | `rgb(0, 0, 0)` | Body text (dark mode base) |
| `--color-white` | `rgb(255, 255, 255)` | Background (light mode base) |

### Secondary colors

| Variable | Value | Usage |
|---|---|---|
| `--color-law-purple` | `rgb(181, 24, 37)` | Secondary accent, hover states |
| `--color-stone` | `rgb(145, 139, 131)` | Muted text, disabled states, borders |
| `--color-charcoal` | `rgb(48, 44, 42)` | Dark surface backgrounds, sidebar |
| `--color-ivory` | `rgb(242, 239, 235)` | Light surface backgrounds, card fills |

## How to use in Tailwind

Reference CSS variables via arbitrary values:

```tsx
// Good
<div className="bg-[var(--color-purple)] text-[var(--color-white)]">

// Bad — never hardcode
<div className="bg-[#3c1053] text-white">
```

Or define Tailwind theme extensions that map to these variables (preferred for reuse):

```ts
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      brand: {
        purple: 'var(--color-purple)',
        red: 'var(--color-red)',
        ...
      }
    }
  }
}
```

## Theme modes

- **Light mode:** white/ivory backgrounds, charcoal/black text, purple accents
- **Dark mode:** charcoal backgrounds, ivory/white text, purple accents
- **Sepia mode:** ivory backgrounds, charcoal text, stone borders

Agents implementing theme switching must use these variables consistently — never hardcode different colors per theme.

## Rules

- **Do not add new color variables** without updating `styles/variables.css` and this document.
- **Do not use Tailwind color utilities** (e.g., `bg-purple-700`) — they do not match the brand palette.
- **Maintain contrast ratios** of at least 4.5:1 for normal text and 3:1 for large text (WCAG 1.4.3).
