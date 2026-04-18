import { expect, test } from "@playwright/test";
import { gotoViewer } from "./helpers";

const viewports = [
  { name: "mobile", width: 390, height: 844 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1440, height: 900 },
] as const;

for (const viewport of viewports) {
  test(`core controls stay usable on ${viewport.name}`, async ({ page }) => {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await gotoViewer(page, { mockMode: "success" });

    await expect(page.getByRole("button", { name: "Previous page" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Next page" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Pages" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Outline" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Next page" })).toBeEnabled();

    await page.getByRole("button", { name: "Next page" }).click();
    await expect(page).toHaveURL(/\/booklets\/hsc-collections\/2(\?.*)?$/);
  });
}
