import { expect, type BrowserContext, type Page } from "@playwright/test";

export const BOOKLET_SLUG = "hsc-collections";
export const ALT_BOOKLET_SLUG = "hsc-vectors";

export const PREF_KEYS = {
  lastUrl: "hsc_last_url",
  scale: "hsc_scale",
};

type PdfResponseMode = "success" | "error";

type ViewerUrlOptions = {
  slug?: string;
  page?: number;
  mockMode?: "off" | "success" | "error";
};

const MINIMAL_PDF = `%PDF-1.1
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 18 Tf
72 72 Td
(Mock PDF) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000202 00000 n 
trailer
<< /Root 1 0 R /Size 5 >>
startxref
294
%%EOF`;

export function viewerUrl(options: ViewerUrlOptions = {}): string {
  const slug = options.slug ?? BOOKLET_SLUG;
  const page = options.page ?? 1;
  const search = new URLSearchParams();

  if (options.mockMode) {
    search.set("e2ePdfMock", options.mockMode);
  }

  const query = search.toString();
  return `/booklets/${slug}/${page}${query ? `?${query}` : ""}`;
}

export async function mockPdfRequests(page: Page, mode: PdfResponseMode = "success"): Promise<void> {
  await page.route("**/*.pdf", async (route) => {
    if (mode === "error") {
      await route.fulfill({
        status: 500,
        contentType: "text/plain",
        body: "mocked pdf load failure",
      });
      return;
    }

    await route.fulfill({
      status: 200,
      contentType: "application/pdf",
      body: Buffer.from(MINIMAL_PDF, "utf8"),
    });
  });
}

export async function gotoViewer(page: Page, options: ViewerUrlOptions = {}): Promise<void> {
  await page.goto(viewerUrl(options));
  await expect(page.getByRole("button", { name: "Previous page" })).toBeVisible();
}

export async function expectViewerShell(page: Page): Promise<void> {
  await expect(page.getByRole("navigation", { name: "Booklet navigation" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Previous page" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Next page" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Pages" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Outline" })).toBeVisible();
  await expect(page.getByRole("contentinfo")).toBeVisible();
}

export async function readZoomPercentage(page: Page): Promise<number> {
  const value = await page.getByTestId("zoom-percentage").innerText();

  const parsed = Number.parseInt(value.replace("%", ""), 10);
  if (Number.isNaN(parsed)) {
    throw new Error(`Unable to parse zoom percentage from: ${value}`);
  }

  return parsed;
}

export async function getCookieValue(context: BrowserContext, name: string): Promise<string | null> {
  const cookies = await context.cookies();
  const match = cookies.find((cookie) => cookie.name === name);
  return match ? decodeURIComponent(match.value) : null;
}
