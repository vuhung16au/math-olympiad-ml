# FAQ

## Why do I see `writing fallback HTML`?

The default `make generate` command is optimized for fast local startup. It gives each booklet only `3000ms` to finish `make4ht`.

If `make4ht` does not finish in time, the generator writes a fallback page instead of failing the app build.

If `make4ht` produces usable HTML but exits non-zero later during DOM post-processing, the generator now tries to salvage that HTML instead of falling back immediately.

## Does `make dev` generate HTML automatically?

No. `make dev` only starts the Next.js web server.

Use one of these when you want to refresh booklet HTML:

```bash
make generate
make generate-html-one BOOKLET=HSC-Collections
make generate-html-all
```

## How do I force a real HTML conversion for one booklet?

```bash
make generate-html-one BOOKLET=HSC-Collections
```

With a custom timeout:

```bash
TIMEOUT_MS=900000 make generate-html-one BOOKLET=HSC-Collections
```

## How do I force a real HTML conversion for all booklets?

```bash
make generate-html-all
```

With a custom timeout:

```bash
TIMEOUT_MS=900000 make generate-html-all
```

## How do I inspect the raw `make4ht` output?

Check:

- `.generated/logs/hsc-collections.log`

One log file is written for each booklet.

## Why do some booklets still show `make4ht failed` even with a long timeout?

There are two common causes:

- `make4ht` produced HTML, but a later DOM-processing step crashed with messages such as `stack overflow`
- graphics-heavy booklets use `tikz` or `pgfplots`, and the converter needs Ghostscript available on `PATH`

The converter now adds Homebrew locations such as `/opt/homebrew/bin` to the `make4ht` environment so `dvisvgm` can find `gs`.

For some booklets, this means the result can now be salvaged as real HTML with warnings instead of being downgraded to a fallback page.

## How long does conversion take on this MacBook Pro M1 Max?

Observed locally on this machine:

- `HSC-Collections` was still running after more than 2 minutes and 50 seconds with a `120000ms` timeout test extended beyond the default fast path.
- This means real conversion is in the **minutes per booklet**, not seconds.

Practical estimate for this machine:

- small booklet: about `1` to `3` minutes
- typical booklet around `100` pages: about `3` to `8` minutes
- harder booklet with heavier graphics or custom environments: about `8` to `15+` minutes

For all listed booklets together, a full pass may take roughly:

- best case: about `45` to `60` minutes
- more realistic mixed case: about `1.5` to `3` hours

These are working estimates, not guaranteed bounds. TikZ, SVG extraction, and custom LaTeX environments can move a booklet toward the slower end.

## Which command should I use day to day?

- use `make generate` for fast dev fallback output
- use `make generate-html-one BOOKLET=...` when you want one booklet converted for real
- use `make generate-html-all` when you want a long full rebuild

## Why did Vercel deploy a fallback page even after I converted `HSC-Collections` locally?

There are two common reasons:

- `make generate` was run later and overwrote `.generated/booklets/hsc-collections.html` with a fallback file
- a normal source deployment did not guarantee that the exact local converted artifact was the one being published

Important finding:

- `make generate` is a fast-path command
- it uses the short `3000ms` timeout
- older builds could overwrite a previously good `HSC-Collections` HTML artifact with fallback HTML

Current workaround/fix:

- `make generate` now preserves an existing successful booklet HTML file if a later fast run falls back
- temporary `tmp/build/logs` data is refreshed, but previously good `.generated/booklets/*.html` and assets are kept unless a new successful conversion replaces them

So if you want the real MathJax HTML for `HSC-Collections`, the safer flow is still:

```bash
make generate-html-one BOOKLET=HSC-Collections
```

Then use `make generate` only as a fast refresh path for the rest of the project.

## What is the safe deployment workflow for `HSC-Collections`?

Use this sequence:

```bash
make generate-html-one BOOKLET=HSC-Collections
make deploy-collections
```

`make deploy-collections` now uses a **prebuilt Vercel deployment** and only exposes `hsc-collections`.

It also refuses to deploy if `.generated/booklets/hsc-collections.html` still contains:

```text
Generated fallback
```

## How do I check whether my local `HSC-Collections` HTML is real or fallback?

Check:

```bash
rg "Generated fallback" .generated/booklets/hsc-collections.html
```

If this command prints a match, the file is fallback HTML.

If there is no match, the file is the converted HTML artifact.

## What if `make deploy-collections` refuses to deploy?

That means the local artifact is still fallback HTML.

Run:

```bash
make generate-html-one BOOKLET=HSC-Collections
```

Then run:

```bash
make deploy-collections
```

## What is the safe deployment workflow for all booklets?

Use this sequence:

```bash
TIMEOUT_MS=900000 make generate-html-all
make build
make deploy-all-prebuilt
```

`make deploy-all-prebuilt`:

- refuses to deploy if any generated booklet still contains `Generated fallback`
- builds a local Vercel prebuilt artifact
- deploys the exact local prebuilt output

## What if `make deploy-all-prebuilt` refuses to deploy?

That means at least one booklet is still fallback HTML.

Run:

```bash
TIMEOUT_MS=900000 make generate-html-all
```

Then inspect the slow or problematic booklets in:

```bash
.generated/logs/
```
