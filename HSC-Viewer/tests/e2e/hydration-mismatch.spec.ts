import { test } from "@playwright/test";
import {
  ALT_BOOKLET_SLUG,
  BOOKLET_SLUG,
  attachHydrationMismatchGuard,
  ensureCookieConsent,
  gotoAndAssertNoHydrationMismatch,
  viewerUrl,
} from "./helpers";

/** Primary routes that SSR client layouts; extend when adding new shells or overlays. */
const CORE_HYDRATION_ROUTES = [
  "/",
  `/booklets/${BOOKLET_SLUG}`,
  viewerUrl({ mockMode: "success", page: 1 }),
  `/booklets/${ALT_BOOKLET_SLUG}?e2ePdfMock=success`,
] as const;

test.describe("Hydration mismatch guard", () => {
  test("core routes emit no hydration mismatch console errors (desktop)", async ({ page }) => {
    const guard = attachHydrationMismatchGuard(page);

    try {
      await ensureCookieConsent(page);

      for (const path of CORE_HYDRATION_ROUTES) {
        await gotoAndAssertNoHydrationMismatch(page, guard, path);
      }
    } finally {
      guard.dispose();
    }
  });

  test("home route without consent cookie still hydrates cleanly", async ({ page }) => {
    const guard = attachHydrationMismatchGuard(page);

    try {
      await gotoAndAssertNoHydrationMismatch(page, guard, "/");
    } finally {
      guard.dispose();
    }
  });

  test("reader and library routes on mobile viewport", async ({ page }) => {
    const guard = attachHydrationMismatchGuard(page);

    try {
      await page.setViewportSize({ width: 390, height: 844 });
      await ensureCookieConsent(page);

      await gotoAndAssertNoHydrationMismatch(page, guard, "/");
      await gotoAndAssertNoHydrationMismatch(
        page,
        guard,
        viewerUrl({ mockMode: "success", page: 1 }),
      );
    } finally {
      guard.dispose();
    }
  });
});
