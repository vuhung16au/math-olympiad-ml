# Regenerate HTML After `.tex` Changes

HTML is derived output. Never edit generated HTML by hand.

`make dev` is independent from generation. It only starts the web server.

For all booklets:

```bash
make generate
```

For all booklets with a longer `make4ht` timeout:

```bash
make generate-html-all
```

For one booklet:

```bash
make generate-one BOOKLET=HSC-Sequences
```

For one booklet with a longer `make4ht` timeout:

```bash
make generate-html-one BOOKLET=HSC-Collections
```

Override the timeout when needed:

```bash
TIMEOUT_MS=900000 make generate-html-one BOOKLET=HSC-Collections
TIMEOUT_MS=900000 make generate-html-all
```

For live local updates:

```bash
make watch
```

The watcher monitors:

- `../HSC-*/**/*.tex`
- `../HSC-Common/styles/**/*`
- `../HSC-Common/assets/**/*`

Each conversion writes a log file to `.generated/logs/<slug>.log`.
