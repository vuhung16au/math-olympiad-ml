import { expect, test } from "@playwright/test";
import { ALT_BOOKLET_SLUG, BOOKLET_SLUG, gotoViewer } from "./helpers";

const HOME_ARIA = "Home – HSC Math Hub";

test.describe("Mobile reader (narrow viewport)", () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test("reader can open menu and navigate to another booklet", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success", slug: BOOKLET_SLUG });

    await page.getByRole("button", { name: "Open booklet navigation" }).click();
    await expect(page.getByRole("complementary", { name: "Mobile booklet navigation" })).toBeVisible();

    const menu = page.getByRole("complementary", { name: "Mobile booklet navigation" });
    const vectorsLink = menu.getByRole("link", { name: "HSC Vectors", exact: true });
    await vectorsLink.scrollIntoViewIfNeeded();
    await vectorsLink.click();
    await expect(page).toHaveURL(new RegExp(`/booklets/${ALT_BOOKLET_SLUG}`));
  });

  test("home link on reader top bar returns to library", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success" });

    await page.getByRole("link", { name: HOME_ARIA, exact: true }).click();
    await expect(page).toHaveURL(/\/$/);
  });

  test("compact toolbar exposes page and zoom; full tools in expanded section", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success" });

    await expect(page.getByRole("button", { name: "Previous page" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Next page" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Zoom in" })).toBeVisible();

    await expect(page.getByRole("button", { name: "Show viewer tools" })).toBeVisible();
    await expect(
      page.locator(".lg\\:hidden").getByText("Share this page", { exact: true }),
    ).toHaveCount(0);

    await page.getByRole("button", { name: "Show viewer tools" }).click();
    await expect(
      page.locator(".lg\\:hidden").getByText("Share this page", { exact: true }),
    ).toBeVisible();
    await expect(page.getByRole("button", { name: "Hide viewer tools" })).toBeVisible();
  });

  test("defaults to single-page mode and renders one mock page", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success", page: 3 });

    await expect(page.getByTestId("mock-pdf-page-3")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-1")).toHaveCount(0);
    await expect(page.getByTestId("mock-pdf-page-2")).toHaveCount(0);
    await expect(page.getByTestId("mock-pdf-page-4")).toHaveCount(0);
  });
});
