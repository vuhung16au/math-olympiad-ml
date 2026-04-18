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
  await expect(page).toHaveURL(new RegExp(`/booklets/${ALT_BOOKLET_SLUG}(/\\d+)?`));
});

test("booklet landing route resumes to saved page for that slug", async ({ page, context }) => {
  await context.addCookies([
    {
      name: PREF_KEYS.lastPageBySlug,
      value: `${ALT_BOOKLET_SLUG}:6,hsc-collections:2`,
      domain: "localhost",
      path: "/",
    },
  ]);

  await page.goto(`/booklets/${ALT_BOOKLET_SLUG}`);
  await expect(page).toHaveURL(new RegExp(`/booklets/${ALT_BOOKLET_SLUG}/6`));
});

test("home route falls back to last slug/page map when last-url is missing", async ({ page, context }) => {
  await context.addCookies([
    {
      name: PREF_KEYS.lastSlug,
      value: ALT_BOOKLET_SLUG,
      domain: "localhost",
      path: "/",
    },
    {
      name: PREF_KEYS.lastPageBySlug,
      value: `${ALT_BOOKLET_SLUG}:4`,
      domain: "localhost",
      path: "/",
    },
  ]);

  await page.goto("/");
  await expect(page).toHaveURL(new RegExp(`/booklets/${ALT_BOOKLET_SLUG}/4`));
});

test("resume mode off keeps booklet landing route at page one", async ({ page, context }) => {
  await context.addCookies([
    {
      name: PREF_KEYS.resumeMode,
      value: "off",
      domain: "localhost",
      path: "/",
    },
    {
      name: PREF_KEYS.lastPageBySlug,
      value: `${ALT_BOOKLET_SLUG}:7`,
      domain: "localhost",
      path: "/",
    },
  ]);

  await page.goto(`/booklets/${ALT_BOOKLET_SLUG}`);
  await expect(page).toHaveURL(new RegExp(`/booklets/${ALT_BOOKLET_SLUG}$`));
});

test("resume mode prompt asks before redirecting", async ({ page, context }) => {
  await context.addCookies([
    {
      name: PREF_KEYS.resumeMode,
      value: "prompt",
      domain: "localhost",
      path: "/",
    },
    {
      name: PREF_KEYS.lastPageBySlug,
      value: `${ALT_BOOKLET_SLUG}:5`,
      domain: "localhost",
      path: "/",
    },
  ]);

  page.once("dialog", (dialog) => dialog.accept());
  await page.goto(`/booklets/${ALT_BOOKLET_SLUG}`);
  await expect(page).toHaveURL(new RegExp(`/booklets/${ALT_BOOKLET_SLUG}/5`));
});
