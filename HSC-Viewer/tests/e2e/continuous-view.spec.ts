import { expect, test } from "@playwright/test";
import { enterStageFullscreen, expectMockPageVisibleInStage, gotoViewer } from "./helpers";

test.describe("Continuous PDF view (desktop)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  test("lazy-loads only nearby pages in continuous mode", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success", page: 1, viewMode: "continuous" });

    await expect(page.getByRole("button", { name: "Continuous view" })).toHaveAttribute("aria-pressed", "true");
    await expect(page.getByTestId("mock-pdf-page-1")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-2")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-3")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-8")).toHaveCount(0);
  });

  test("fullscreen pages and outline navigator jump to expected targets", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success", page: 1, viewMode: "continuous" });

    await enterStageFullscreen(page);

    await page.getByRole("button", { name: "Jump to page 4" }).click();
    await expectMockPageVisibleInStage(page, 4);
    await expect(page).toHaveURL(/\/booklets\/hsc-collections\/4(\?.*)?$/);

    await page.getByRole("button", { name: "Outline" }).click();
    await expect(page.getByRole("list", { name: "PDF outline list" })).toBeVisible();

    await page.getByRole("button", { name: /Jump to Chapter 2 on page 4/i }).click();
    await expectMockPageVisibleInStage(page, 4);
    await expect(page).toHaveURL(/\/booklets\/hsc-collections\/4(\?.*)?$/);
  });
});
