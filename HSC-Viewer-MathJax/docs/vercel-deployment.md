# Build And Deploy On Vercel

## Quick source deploy

```bash
make deploy
```

This runs:

```bash
bunx vercel --prod
```

Use this only when you are happy with a normal source deployment.

## Safer full deployment

Generate all booklet HTML first:

```bash
TIMEOUT_MS=900000 make generate-html-all
make build
make deploy-all-prebuilt
```

`make deploy-all-prebuilt`:

- checks that `.generated/booklets/*.html` are not fallback pages
- builds a local Vercel prebuilt artifact
- deploys the exact local prebuilt output

## Safer single-booklet deployment

```bash
make generate-html-one BOOKLET=HSC-Collections
make deploy-collections
```
