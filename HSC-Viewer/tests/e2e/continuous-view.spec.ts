import { expect, test } from "@playwright/test";
import { gotoViewer } from "./helpers";

test.describe("Continuous PDF view (desktop)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  test("lazy-loads only nearby pages in continuous mode", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success", page: 1 });

    await expect(page.getByRole("button", { name: "Continuous view" })).toHaveAttribute("aria-pressed", "true");
    await expect(page.getByTestId("mock-pdf-page-1")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-2")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-3")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-8")).toHaveCount(0);
  });
});
