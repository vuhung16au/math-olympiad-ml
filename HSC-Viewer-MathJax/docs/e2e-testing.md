# E2E Testing

Playwright is used for smoke coverage.

Run tests:

```bash
cd HSC-Viewer-MathJax
make test
```

Before adding a new booklet, confirm:

- home page loads
- booklet appears in sidebar or landing list
- booklet route opens
- generated reader content is visible

If tests fail because HTML is stale, run `make generate` first.
