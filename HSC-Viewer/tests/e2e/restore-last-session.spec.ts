import { expect, test } from "@playwright/test";
import { ALT_BOOKLET_SLUG, PREF_KEYS } from "./helpers";

test("home route restores last opened booklet from cookie", async ({ page, context }) => {
  await context.addCookies([
    {
      name: PREF_KEYS.lastUrl,
      value: `/booklets/${ALT_BOOKLET_SLUG}/3?e2ePdfMock=success`,
      domain: "localhost",
      path: "/",
    },
  ]);

  await page.goto("/");
  await expect(page).toHaveURL(new RegExp(`/booklets/${ALT_BOOKLET_SLUG}/3`));
});
