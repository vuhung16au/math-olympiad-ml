# Build And Run Locally

```bash
cd HSC-Viewer-MathJax
make install
make dev
```

Useful commands:

- `make dev` only starts the web server. It does not generate HTML.
- `make generate` refreshes the fast fallback/generated HTML output.
- `make generate-html-all` runs a longer full conversion attempt for all booklets.
- `make watch` watches `.tex` and shared style changes.
- `make build` runs generation first, then `next build`.
- `make clean` removes local generated and Next.js artifacts.

If a booklet page looks stale, run `make generate` again.
