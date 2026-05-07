import { expect, test } from "@playwright/test";

test("home page lists booklets", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("Browse HSC booklet content online")).toBeVisible();
  await expect(
    page.locator("main").getByRole("link", { name: /HSC Collections/ }).last(),
  ).toBeVisible();
});

test("booklet route renders generated reader", async ({ page }) => {
  await page.goto("/booklets/hsc-collections");
  await expect(
    page.locator("main").getByRole("heading", { name: "HSC Collections", level: 2 }),
  ).toBeVisible();
  await expect(page.getByText("Generated fallback")).toBeVisible();
});
