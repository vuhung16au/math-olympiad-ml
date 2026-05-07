# Add A New Booklet

When adding `HSC-new-booklet`:

1. Add the new folder at the repo root with its main `.tex` file.
2. Register it in [lib/booklets.ts](../lib/booklets.ts).
3. Set:
   - `title`
   - `slug`
   - `sourceDir`
   - `entryTex`
   - `order`
   - `isAvailable`
4. Run:

```bash
make generate-one BOOKLET=HSC-new-booklet
make dev
```

5. Verify the booklet appears in the sidebar and its page opens.
