# System Architecture

`HSC-Viewer-MathJax` converts sibling `HSC-xxx` LaTeX projects into generated HTML, then serves that output with Next.js.

## System context

```mermaid
flowchart LR
  A["HSC-xxx .tex sources"] --> B["make4ht conversion"]
  B --> C["post-processing and sanitization"]
  C --> D[".generated manifest and HTML"]
  D --> E["Next.js app"]
  E --> F["Browser with MathJax"]
```

## Conversion pipeline

```mermaid
flowchart TD
  A["make generate"] --> B["scripts/generate-booklets.ts"]
  B --> C["make4ht per booklet"]
  C --> D["sanitize and rewrite assets"]
  D --> E["write .generated/booklets/*.html"]
  D --> F["write .generated/assets/*"]
  E --> G["write .generated/manifest.json"]
```

## Runtime flow

```mermaid
flowchart TD
  A["User opens /booklets/[slug]"] --> B["Next.js reads manifest"]
  B --> C["Server loads generated HTML"]
  C --> D["Reader renders content"]
  D --> E["MathJax typesets formulas"]
  E --> F["User reads booklet"]
```
