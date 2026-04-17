# HSC Math Hub

HSC Math Hub is a Next.js app for browsing and reading the HSC mathematics PDF booklets hosted in this repository.

The viewer loads PDFs directly from `raw.githubusercontent.com` so the browser receives the correct content type and can display each booklet inline.

## Features

- responsive booklet library with sidebar navigation and mobile menu
- in-browser PDF reading with `react-pdf`
- page navigation, zoom, fit-width, download, print, and fullscreen actions
- disabled `HSC-Sequences` entry until its PDF is published
- Vercel Analytics for page views and reader interactions

## Stack

- Next.js App Router
- React 19
- Tailwind CSS
- react-pdf
- Vercel deployment and analytics
- Bun for package management

## License

The content and project are distributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Development

```bash
cd HSC-Viewer
make install
make dev
```

For deployment and thumbnail generation details, see [QUICKSTART.md](./QUICKSTART.md).
