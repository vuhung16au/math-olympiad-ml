import { expect, test } from "@playwright/test";
import { PREF_KEYS, getCookieValue, gotoViewer } from "./helpers";

test("next/previous/page input updates route and last-url cookie", async ({ page, context }) => {
  await gotoViewer(page, { page: 1, mockMode: "success" });
  await expect(page.getByRole("button", { name: "Next page" })).toBeEnabled();

  await page.getByRole("button", { name: "Single page view" }).click();

  const pageInput = page.getByTestId("page-number-input");
  await pageInput.click();
  await pageInput.fill("2");
  await pageInput.press("Enter");
  await expect(page).toHaveURL(/\/booklets\/hsc-collections\/2(\?.*)?$/);

  await page.getByRole("button", { name: "Next page" }).click();
  await expect(page).toHaveURL(/\/booklets\/hsc-collections\/3(\?.*)?$/);

  await page.getByRole("button", { name: "Previous page" }).click();
  await expect(page).toHaveURL(/\/booklets\/hsc-collections\/2(\?.*)?$/);

  await pageInput.click();
  await pageInput.fill("5");
  await pageInput.press("Enter");

  await expect(page).toHaveURL(/\/booklets\/hsc-collections\/5(\?.*)?$/);

  const lastUrl = await getCookieValue(context, PREF_KEYS.lastUrl);
  expect(lastUrl).toContain("/booklets/hsc-collections/5");

  const lastSlug = await getCookieValue(context, PREF_KEYS.lastSlug);
  expect(lastSlug).toBe("hsc-collections");

  const lastPageBySlug = await getCookieValue(context, PREF_KEYS.lastPageBySlug);
  expect(lastPageBySlug).toContain("hsc-collections:5");
});
