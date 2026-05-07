# HSC-Viewer-MathJax

HSC-Viewer-MathJax is a Next.js app that reads the root `HSC-xxx` LaTeX projects, converts them to HTML with `make4ht`, and serves them online with MathJax-style rendering.

The `.tex` files remain the single source of truth. Generated HTML lives under `.generated/`.

## Quick start

```bash
cd HSC-Viewer-MathJax
make install
make generate
make dev
```

See [QUICKSTART.md](./QUICKSTART.md) and the short docs in [docs](./docs).
