import { test, expect } from "@playwright/test";
import { mockPdfRequests, expectViewerShell, expectMockPageVisibleInStage } from "./helpers";

test.describe("SEO and Marketing Tests", () => {
  test("sitemap.xml is available and contains expected URLs", async ({ request }) => {
    const res = await request.get('/sitemap.xml');
    expect(res.status(), "sitemap should return 200").toBe(200);
    const xml = await res.text();
    expect(xml).toContain('<?xml');
    expect(xml).toContain('<urlset');
    expect(xml).toContain('<loc>https://hsc-math-hub.vercel.app</loc>');
    expect(xml).toContain('<loc>https://hsc-math-hub.vercel.app/booklets/hsc-collections</loc>');
  });

  test("homepage and booklet pages contain SEO keywords", async ({ page }) => {
    // Test homepage
    await page.goto('/');
    const homeKeywords = await page.locator('meta[name="keywords"]').getAttribute('content');
    expect(homeKeywords).toContain('HSC Maths');
    expect(homeKeywords).toContain('Extension 1');
    expect(homeKeywords).toContain('Extension 2');

    // Test a booklet page
    await page.goto('/booklets/hsc-collections/0');
    const bookletKeywords = await page.locator('meta[name="keywords"]').getAttribute('content');
    expect(bookletKeywords).toContain('HSC Mathematics');
    expect(bookletKeywords).toContain('Extension 1');
  });

  test("footer links are present and correct", async ({ page }) => {
    await page.goto('/');
    
    const footer = page.locator('footer');
    await expect(footer).toBeVisible();
    
    const substackLink = footer.locator('a:has-text("Substack")');
    await expect(substackLink).toHaveAttribute('href', 'https://vuhung16.substack.com/');
    
    const faqLink = footer.locator('a:has-text("FAQ")');
    await expect(faqLink).toHaveAttribute('href', '/faq');

    const linkedinLink = footer.locator('a:has-text("LinkedIn")');
    await expect(linkedinLink).toHaveAttribute('href', 'https://www.linkedin.com/in/nguyenvuhung/');

    const githubLink = footer.locator('a:has-text("Source repository")');
    await expect(githubLink).toHaveAttribute('href', 'https://github.com/vuhung16au/math-olympiad-ml');
  });

  test("last page shows Substack CTA popup", async ({ page }) => {
    // Navigate to the last page of hsc-collections (page 56, since there are 57 pages)
    await page.goto('/booklets/hsc-collections/56');
    
    await expectViewerShell(page);
    
    // The Substack CTA popup should appear since we are on the last page
    const popup = page.getByText("Join Substack Channel");
    await expect(popup).toBeVisible();
  });

  test("booklet page contains valid JSON-LD", async ({ page }) => {
    await page.goto('/booklets/hsc-collections');
    const jsonLdScript = await page.locator('script[type="application/ld+json"]').textContent();
    expect(jsonLdScript).toBeTruthy();
    
    if (jsonLdScript) {
      const jsonLd = JSON.parse(jsonLdScript);
      expect(jsonLd['@context']).toBe('https://schema.org');
      expect(jsonLd['@type']).toBe('Course');
      expect(jsonLd.educationalLevel).toBe('NSW HSC');
    }
  });
});

