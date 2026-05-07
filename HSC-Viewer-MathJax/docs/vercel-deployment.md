# Build And Deploy On Vercel

Local release flow:

```bash
cd HSC-Viewer-MathJax
make build
make deploy
```

`make deploy` is an alias for `make deploy-vercel`, which runs:

```bash
bunx vercel --prod
```

Vercel uses:

- install command: `bun install`
- build command: `make build`

That means HTML is regenerated from `.tex` during deployment.
