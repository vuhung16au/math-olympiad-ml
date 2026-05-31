import { expect, test } from "@playwright/test";
import {
  PREF_KEYS,
  ensureCookieConsent,
  expectContinuousViewActive,
  expectSinglePageViewActive,
  gotoViewer,
  viewerUrl,
} from "./helpers";

test.describe("Default PDF view mode (desktop)", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  test("first visit opens in continuous view", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success", page: 1 });

    await expectContinuousViewActive(page);
    await expect(page.getByTestId("mock-pdf-page-1")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-2")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-3")).toBeVisible();
  });

  test("saved single-page preference is restored from cookie", async ({ page, context }) => {
    await ensureCookieConsent(page);
    await context.addCookies([
      {
        name: PREF_KEYS.viewMode,
        value: "single",
        domain: "localhost",
        path: "/",
      },
    ]);

    await page.goto(viewerUrl({ mockMode: "success", page: 3 }));
    await expect(page.getByRole("button", { name: "Previous page" })).toBeVisible();
    await expectSinglePageViewActive(page);
    await expect(page.getByTestId("mock-pdf-page-3")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-2")).toHaveCount(0);
    await expect(page.getByTestId("mock-pdf-page-4")).toHaveCount(0);
  });
});

test.describe("Default PDF view mode (mobile)", () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test("first visit opens in continuous view", async ({ page }) => {
    await gotoViewer(page, { mockMode: "success", page: 3 });

    await page.getByRole("button", { name: "Show viewer tools" }).click();
    await expect(page.getByRole("button", { name: "Hide viewer tools" })).toBeVisible();
    await expectContinuousViewActive(page);

    await expect(page.getByTestId("mock-pdf-page-3")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-2")).toBeVisible();
    await expect(page.getByTestId("mock-pdf-page-4")).toBeVisible();
  });
});
