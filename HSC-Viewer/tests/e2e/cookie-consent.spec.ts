import { expect, test } from "@playwright/test";
import { PREF_KEYS, getCookieValue } from "./helpers";

test.describe("Cookie consent banner", () => {
  test("shows on first visit; Accept stores consent and hides the banner", async ({ page, context }) => {
    await page.goto("/");
    const consent = page.getByTestId("cookie-consent-banner");
    await expect(consent).toBeVisible();
    await expect(consent).toContainText("cookies");

    await page.getByRole("button", { name: "Accept and dismiss cookie notice" }).click();
    await expect(consent).toBeHidden();

    const stored = await getCookieValue(context, PREF_KEYS.cookieConsent);
    expect(stored).toBe("1");
  });

  test("does not show when consent cookie is already set", async ({ page, context }) => {
    await context.addCookies([
      {
        name: PREF_KEYS.cookieConsent,
        value: "1",
        domain: "localhost",
        path: "/",
      },
    ]);

    await page.goto("/");
    await expect(page.locator('[data-testid="cookie-consent-banner"]')).toHaveCount(0);
  });
});
