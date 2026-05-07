# FAQ

## Why do I see `writing fallback HTML`?

The default `make generate` command is optimized for fast local startup. It gives each booklet only `3000ms` to finish `make4ht`.

If `make4ht` does not finish in time, the generator writes a fallback page instead of failing the app build.

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
