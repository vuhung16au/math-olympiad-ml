# Keyboard Shortcuts Policy

## Purpose

Power users — students reviewing problems under time pressure — benefit from fast keyboard navigation. All shortcuts listed here must be implemented and kept functional.

## Shortcut map

### Navigation

| Shortcut | Action |
|---|---|
| `→` or `j` | Next page |
| `←` or `k` | Previous page |
| `g` then `g` | Go to first page |
| `G` | Go to last page |
| `Ctrl+G` / `Cmd+G` | Open "Go to page" input |

### Zoom

| Shortcut | Action |
|---|---|
| `+` or `=` | Zoom in |
| `-` | Zoom out |
| `0` | Reset zoom to fit-width |

### View

| Shortcut | Action |
|---|---|
| `f` | Toggle fullscreen |
| `s` | Toggle sidebar |
| `t` | Cycle theme (light → dark → sepia → light) |
| `?` | Open shortcut help overlay |

### Document actions

| Shortcut | Action |
|---|---|
| `Ctrl+P` / `Cmd+P` | Print |
| `Ctrl+S` / `Cmd+S` | Download PDF |

## Implementation rules

- Register shortcuts at the `document` level using `keydown` events.
- **Suppress shortcuts when focus is inside an `<input>`, `<textarea>`, or `[contenteditable]`** to avoid conflicts with text entry.
- All shortcuts must be listed in a keyboard help overlay, toggled by `?`. The overlay must be keyboard accessible and closeable with `Escape`.
- Shortcuts must not conflict with browser-reserved shortcuts (`Ctrl+W`, `Ctrl+T`, etc.).
- When a shortcut is invoked, provide brief visual feedback (e.g., a transient toast or a highlighted toolbar button).

## Discovery

- The toolbar "Keyboard shortcuts" button (icon: keyboard) must open the help overlay.
- The help overlay must also be triggered by pressing `?`.
- On first visit (no `shortcuts-seen` cookie), show a dismissible hint banner: "Press ? for keyboard shortcuts."

## Testing

Add e2e tests in `tests/e2e/` for any new shortcut. Verify:
1. The action occurs correctly.
2. The shortcut is suppressed while a text input is focused.
3. The help overlay opens and closes correctly.
