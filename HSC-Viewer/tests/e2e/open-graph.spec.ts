import { test, expect } from "@playwright/test";

function getOgMeta(html: string, property: string): string | null {
  // Matches: <meta property="og:..." content="...">
  const re = new RegExp(
    `<meta\\s+[^>]*property=[\\"']${property.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&")}[\\"'][^>]*content=[\\"']([^\\\"']*)[\\\"'][^>]*>`,
    "i",
  );
  const match = html.match(re);
  return match?.[1] ?? null;
}

function getOgName(html: string, name: string): string | null {
  // Matches: <meta name="..." content="..."> (used by some renderers)
  const re = new RegExp(
    `<meta\\s+[^>]*name=[\\"']${name.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&")}[\\"'][^>]*content=[\\"']([^\\\"']*)[\\\"'][^>]*>`,
    "i",
  );
  const match = html.match(re);
  return match?.[1] ?? null;
}

test("booklet page includes OG meta in initial HTML and image endpoint returns PNG", async ({ request, baseURL }) => {
  const url = "/booklets/hsc-last-resorts/97";
  const res = await request.get(url);
  expect(res.status(), "expected booklet page to return 200").toBe(200);
  const html = await res.text();

  const ogTitle = getOgMeta(html, "og:title");
  const ogDescription = getOgMeta(html, "og:description");
  const ogUrl = getOgMeta(html, "og:url");
  const ogImage = getOgMeta(html, "og:image");
  const ogType = getOgMeta(html, "og:type");
  const ogSiteName = getOgMeta(html, "og:site_name");

  expect(ogTitle).toContain("HSC Last Resorts");
  expect(ogTitle).toContain("Page 97");
  expect(ogDescription).toBeTruthy();
  expect(ogType).toBe("website");
  expect(ogSiteName).toBe("HSC Math Hub");

  // URL should be absolute and match the requested route.
  expect(ogUrl).toBe(`https://hsc-math-hub.vercel.app${url}`);

  expect(ogImage).toBeTruthy();
  expect(ogImage?.startsWith("https://")).toBe(true);
  expect(ogImage).toContain("/og/booklets/hsc-last-resorts/97.png");

  // Width/height can be rendered as og:image:width / og:image:height or name equivalents.
  const ogWidth = getOgMeta(html, "og:image:width") ?? getOgName(html, "og:image:width");
  const ogHeight = getOgMeta(html, "og:image:height") ?? getOgName(html, "og:image:height");
  expect(ogWidth).toBe("1200");
  expect(ogHeight).toBe("630");

  const imagePath = new URL(ogImage ?? "", baseURL ?? "http://localhost:3000").pathname +
    new URL(ogImage ?? "", baseURL ?? "http://localhost:3000").search;

  const imgRes = await request.get(imagePath);
  expect(imgRes.status()).toBe(200);
  expect(imgRes.headers()["content-type"]).toContain("image/png");
});

test("invalid slug returns 404 but includes Not-found OG meta", async ({ request }) => {
  const url = "/booklets/does-not-exist/1";
  const res = await request.get(url);
  expect(res.status(), "expected invalid slug route to return 404").toBe(404);
  const html = await res.text();

  expect(getOgMeta(html, "og:title")).toBe("Page not found — HSC Math Hub");
  expect(getOgMeta(html, "og:description")).toContain("does not exist");
  expect(getOgMeta(html, "og:image")).toContain("/og/site-fallback.png");
});

test("out-of-range page returns 404 but includes Not-found OG meta", async ({ request }) => {
  const url = "/booklets/hsc-last-resorts/9999";
  const res = await request.get(url);
  expect(res.status(), "expected out-of-range route to return 404").toBe(404);
  const html = await res.text();

  expect(getOgMeta(html, "og:title")).toBe("Page not found — HSC Math Hub");
  expect(getOgMeta(html, "og:image")).toContain("/og/site-fallback.png");
});

