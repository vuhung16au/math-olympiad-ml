import { expect, test } from "@playwright/test";
import { PREF_KEYS, getCookieValue, gotoViewer, readZoomPercentage } from "./helpers";

test("toolbar actions expose tooltips and zoom state persists through cookie", async ({ page, context }) => {
  await gotoViewer(page, { mockMode: "success" });

  const zoomIn = page.getByRole("button", { name: "Zoom in" });
  const zoomOut = page.getByRole("button", { name: "Zoom out" });
  const resetZoom = page.getByRole("button", { name: "Reset zoom" });
  const fullscreen = page.getByRole("button", { name: "Fullscreen" });

  await expect(zoomIn).toHaveAttribute("title", "Zoom in");
  await expect(zoomOut).toHaveAttribute("title", "Zoom out");
  await expect(resetZoom).toHaveAttribute("title", "Reset zoom");
  await expect(fullscreen).toHaveAttribute("title", "Fullscreen");

  const initialZoom = await readZoomPercentage(page);

  await zoomIn.click();
  await expect.poll(async () => readZoomPercentage(page)).toBe(initialZoom + 20);

  await zoomOut.click();
  await expect.poll(async () => readZoomPercentage(page)).toBe(initialZoom);

  await zoomIn.click();
  await expect.poll(async () => readZoomPercentage(page)).toBe(initialZoom + 20);

  const scaleCookie = await getCookieValue(context, PREF_KEYS.scale);
  expect(scaleCookie).toBe(String((initialZoom + 20) / 100));

  await page.reload();
  await expect.poll(async () => readZoomPercentage(page)).toBe(initialZoom + 20);

  await resetZoom.click();
  await expect.poll(async () => readZoomPercentage(page)).toBe(150);
});
