# Command-line tools

## TeX export (`export:tex`)

Generate **TikZ** (`.tikz` picture fragment) and/or **standalone LaTeX** (`.tex` using the `standalone` class) for any preset. This uses the same export logic as the web API (`app/lib/server-export-tex.ts`).

### Requirements

- Node.js 18+
- Dependencies installed (`npm install`), including dev dependency `tsx`

### Default mode

With **no** `--family` or `--preset`, exports **one default preset per family** (IFS, L-system, escape-time, Newton, attractor, inversion) into `artifacts/tex/`:

```bash
npm run export:tex
```

### Help

```bash
npx tsx scripts/export-fractals-tex.ts --help
```

### Advanced usage

| Option | Description |
|--------|-------------|
| `--family` | `ifs`, `lsystem`, `escape-time`, `newton`, `attractor`, `inversion`, or `all` |
| `--preset` | Preset id, or `all` for every preset in the selected family |
| `--format` | `tikz`, `tex`, or `both` (default: `both`) |
| `--out <dir>` | Output root (default: `artifacts/tex`) |
| `--width`, `--height` | Reference render size (default 1280×720) |
| `--size WxH` | Shorthand for width×height |
| `--scheme <name>` | `acu`, `matrix`, `emerald`, `ink` (maps to API `mainColorScheme`) |
| `--bg <hex>` | Background `#RRGGBB` |
| `--tex-max-dim <n>` | Cap longest side for raster-based families in the TeX exporter (escape-time, Newton, attractors, inversion) |
| `--param key=value` | Extra parameters (repeatable); same keys as the HTTP API query string / web form |

**Family `all` behavior**

- `--family all` **without** `--preset`: one default preset per family (lightweight).
- `--family all --preset all`: every preset in every family (large run).
- `--family all --preset fern`: only families that define preset `fern`.

### Examples

```bash
# Single IFS preset, TikZ only
npm run export:tex -- --family ifs --preset fern --format tikz --out ./out-tex

# All L-system presets as standalone LaTeX
npm run export:tex -- --family lsystem --preset all --format tex

# Custom IFS parameters
npm run export:tex -- --family ifs --preset fern --param ifsIterations=80000 --param ifsDensity=70
```

Outputs are written under `<out>/<family>/<preset>.tikz` and/or `<preset>.tex`.

### Compiling standalone `.tex`

Use a LaTeX install with TikZ (e.g. TeX Live):

```bash
pdflatex my-fractal.tex
```

Each dot uses PGF’s `\\pgfinterruptpath`…`\\endpgfinterruptpath` around `\\fill … circle` so paths are not merged into one huge soft path (which can exhaust pdfTeX memory even with `scope`). Long L-system polylines are split into several `\\draw` lines for the input-buffer limit.

For very dense raster exports, `lualatex` may compile faster or with higher limits than `pdflatex`.

## Booklet mattes (`generate:booklet-mattes`)

Produces **twenty lightweight** TikZ snippets plus `matte.tex` and `Makefile` under `artifacts/booklet-mattes/`: **IFS** (scatter dots on white) and **L-system** curves only (white rectangle + `\draw` strokes)—no raster escape-time / Newton mattes so backgrounds stay printable white. Reference raster aspect uses **A4 portrait** (**595×842** PDF points, same as `a4paper`); **`--tex-max-dim`** remains small so runs stay lightweight if you add raster exports later. Then:

```bash
npm run generate:booklet-mattes
make -C artifacts/booklet-mattes pdf   # LuaLaTeX compiles matte.tex
```

Requires a normal local install of `tsx` (the script invokes `tsx` to run [`scripts/export-fractals-tex.ts`](../scripts/export-fractals-tex.ts)). Sandboxed or hardened environments that disallow `tsx` IPC may fail; run from your usual developer shell inside the repo.

## Other scripts

| Command | Purpose |
|---------|---------|
| `npm run generate:booklet-mattes` | 20 small TikZ mattes + `matte.tex` / `Makefile` in `artifacts/booklet-mattes/` |
| `node scripts/generate-all-fractals.js` | Raster PNG catalog into `artifacts/` |
| `npm run test:fractals:playwright` | UI sweep via Playwright |
| `npm run docs:fractals` | Regenerate fractal docs |

See [README.md](../README.md) for the full list.
