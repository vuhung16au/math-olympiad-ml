# Booklet Settings

Main booklet settings live in [lib/booklets.ts](../lib/booklets.ts).

Important fields:

- `title`: sidebar and page title
- `slug`: route segment
- `sourceDir`: root LaTeX folder
- `entryTex`: main `.tex` entry file
- `order`: sidebar order
- `isAvailable`: visibility/readiness flag

Main colors live in [styles/variables.css](../styles/variables.css).

To change booklet order, title, slug, or source mapping, update the registry and regenerate HTML.
