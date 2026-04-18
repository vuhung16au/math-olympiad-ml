import { expect, test } from "@playwright/test";
import { getCookieValue, gotoViewer, PREF_KEYS } from "./helpers";

test("pages and outline navigator jump to expected targets", async ({ page }) => {
  await gotoViewer(page, { mockMode: "success" });

  await page.getByRole("button", { name: "Jump to page 6" }).click();
  await expect(page).toHaveURL(/\/booklets\/hsc-collections\/6(\?.*)?$/);

  await page.getByRole("button", { name: "Outline" }).click();
  await expect(page.getByRole("list", { name: "PDF outline list" })).toBeVisible();

  await page.getByRole("button", { name: /Jump to Chapter 2 on page 4/i }).click();
  await expect(page).toHaveURL(/\/booklets\/hsc-collections\/4(\?.*)?$/);
});

test("outline tab persists via cookie", async ({ page, context }) => {
  await gotoViewer(page, { mockMode: "success" });

  await page.getByRole("button", { name: "Outline" }).click();
  await expect(page.getByRole("button", { name: "Outline" })).toHaveAttribute("aria-pressed", "true");

  await expect.poll(async () => getCookieValue(context, PREF_KEYS.outlineTab)).toBe("outline");

  await page.reload();
  await expect(page.getByRole("button", { name: "Outline" })).toHaveAttribute("aria-pressed", "true");
});

test("navigator position restores from cookie", async ({ page, context }) => {
  await context.addCookies([
    {
      name: PREF_KEYS.navPanelPos,
      value: "120,90",
      domain: "localhost",
      path: "/",
    },
  ]);

  await gotoViewer(page, { mockMode: "success" });

  const sidebar = page.getByLabel("PDF navigation sidebar");
  await expect(sidebar).toHaveAttribute("style", /left:\s*120px;\s*top:\s*90px;/i);
});
