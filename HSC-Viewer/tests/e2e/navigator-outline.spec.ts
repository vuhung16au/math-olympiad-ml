import { expect, test } from "@playwright/test";
import { gotoViewer } from "./helpers";

test("pages and outline navigator jump to expected targets", async ({ page }) => {
  await gotoViewer(page, { mockMode: "success" });

  await page.getByRole("button", { name: "Jump to page 6" }).click();
  await expect(page).toHaveURL(/\/booklets\/hsc-collections\/6(\?.*)?$/);

  await page.getByRole("button", { name: "Outline" }).click();
  await expect(page.getByRole("list", { name: "PDF outline list" })).toBeVisible();

  await page.getByRole("button", { name: /Jump to Chapter 2 on page 4/i }).click();
  await expect(page).toHaveURL(/\/booklets\/hsc-collections\/4(\?.*)?$/);
});
