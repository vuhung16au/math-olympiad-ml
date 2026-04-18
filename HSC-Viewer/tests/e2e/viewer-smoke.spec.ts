import { test } from "@playwright/test";
import { expectViewerShell, gotoViewer } from "./helpers";

test("viewer shell renders core reader UI", async ({ page }) => {
  await gotoViewer(page, { mockMode: "success" });
  await expectViewerShell(page);
});
