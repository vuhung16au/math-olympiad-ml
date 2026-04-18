import { expect, test } from "@playwright/test";
import { viewerUrl } from "./helpers";

test("shows user-facing error state when PDF fails to load", async ({ page }) => {
  await page.goto(viewerUrl({ mockMode: "error" }));

  await expect(page.getByText("Failed to load PDF.")).toBeVisible();
  await expect(page.getByRole("link", { name: "Open raw PDF" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Next page" })).toBeVisible();
});
