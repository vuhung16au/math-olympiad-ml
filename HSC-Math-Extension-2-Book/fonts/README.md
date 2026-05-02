## Samarkan font (optional)

Booklets that use `\ramanujanfont` load **Samarkan** from the shared folder [`../../HSC-Common/fonts/`](../../HSC-Common/fonts/) (filename `SAMAN___.TTF`). If the font file is not present, the PDF still compiles under pdfLaTeX, but `\ramanujanfont` has no effect.

## How to get the font

- **Download**: get “Samarkan Font” from `https://www.fontmagic.com/samarkan.font` or `https://www.dafont.com/font-comment.php?file=samarkan`
- **Place it here**: copy the `.ttf` to `HSC-Common/fonts/SAMAN___.TTF` (exact name)
- You can also install the font system-wide (optional).

## How to compile (embed the font)

`fontspec` requires **LuaLaTeX** or **XeLaTeX**. Use each booklet’s `Makefile` (`make pdf`).

## Licensing note (important)

Samarkan is **shareware / not freely usable**. Use it only under the font’s license/terms.
