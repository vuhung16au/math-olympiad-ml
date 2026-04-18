import { expect, test } from "@playwright/test";
import { gotoViewer, mockPdfRequests, viewerUrl } from "./helpers";

test("pdf page wrapper shrink-wraps to rendered layer width", async ({ page }) => {
  await mockPdfRequests(page, "success");
  await page.goto(viewerUrl({ mockMode: "off" }));
  const firstPdfPage = page.locator(".react-pdf__Page").first();
  await expect(firstPdfPage.locator(".react-pdf__Page__canvas")).toBeVisible();

  const metrics = await firstPdfPage.evaluate((pageElement) => {
    const canvas = pageElement.querySelector(".react-pdf__Page__canvas");
    const textLayer = pageElement.querySelector(".react-pdf__Page__textContent");

    if (!(canvas instanceof HTMLElement)) {
      throw new Error("Canvas layer not found");
    }

    const pageRect = pageElement.getBoundingClientRect();
    const canvasRect = canvas.getBoundingClientRect();
    const textRect = textLayer instanceof HTMLElement ? textLayer.getBoundingClientRect() : null;

    return {
      pageWidth: pageRect.width,
      canvasWidth: canvasRect.width,
      textWidth: textRect?.width ?? null,
    };
  });

  expect(Math.abs(metrics.pageWidth - metrics.canvasWidth)).toBeLessThan(1);

  if (metrics.textWidth !== null) {
    expect(Math.abs(metrics.textWidth - metrics.canvasWidth)).toBeLessThan(1);
  }
});

test("viewer shell still renders with mock mode", async ({ page }) => {
  await gotoViewer(page, { mockMode: "success" });
  await expect(page.getByRole("button", { name: "Previous page" })).toBeVisible();
});

test("real TOC link annotations stay inside the rendered page bounds", async ({ page }) => {
  await page.goto("/booklets/hsc-combinatorics/4");

  const tocPage = page.locator('.react-pdf__Page[data-page-number="4"]').first();
  const firstAnnotation = tocPage.locator(".react-pdf__Page__annotations section").first();

  await expect(tocPage.locator(".react-pdf__Page__canvas")).toBeVisible();
  await expect(firstAnnotation).toBeVisible();

  const metrics = await tocPage.evaluate((pageElement) => {
    const canvas = pageElement.querySelector(".react-pdf__Page__canvas");
    const annotationLayer = pageElement.querySelector(".react-pdf__Page__annotations");
    const annotation = pageElement.querySelector(".react-pdf__Page__annotations section");

    if (!(canvas instanceof HTMLElement) || !(annotationLayer instanceof HTMLElement) || !(annotation instanceof HTMLElement)) {
      throw new Error("Expected PDF layers were not found");
    }

    const pageRect = pageElement.getBoundingClientRect();
    const canvasRect = canvas.getBoundingClientRect();
    const annotationLayerRect = annotationLayer.getBoundingClientRect();
    const annotationRect = annotation.getBoundingClientRect();

    return {
      pageWidth: pageRect.width,
      canvasWidth: canvasRect.width,
      annotationLayerWidth: annotationLayerRect.width,
      annotationLeft: annotationRect.left - pageRect.left,
      annotationRight: annotationRect.right - pageRect.left,
    };
  });

  expect(Math.abs(metrics.pageWidth - metrics.canvasWidth)).toBeLessThan(1);
  expect(Math.abs(metrics.annotationLayerWidth - metrics.canvasWidth)).toBeLessThan(1);
  expect(metrics.annotationLeft).toBeGreaterThanOrEqual(-1);
  expect(metrics.annotationRight).toBeLessThanOrEqual(metrics.canvasWidth + 1);
});

test("real TOC link annotations do not render embedded PDF borders", async ({ page }) => {
  await page.goto("/booklets/hsc-functions/4");

  const firstAnnotation = page
    .locator('.react-pdf__Page[data-page-number="4"] .react-pdf__Page__annotations .linkAnnotation')
    .first();

  await expect(firstAnnotation).toBeVisible();

  const styles = await firstAnnotation.evaluate((element) => {
    const computed = getComputedStyle(element);
    return {
      borderTopWidth: computed.borderTopWidth,
      borderRightWidth: computed.borderRightWidth,
      borderBottomWidth: computed.borderBottomWidth,
      borderLeftWidth: computed.borderLeftWidth,
      boxShadow: computed.boxShadow,
    };
  });

  expect(styles.borderTopWidth).toBe("0px");
  expect(styles.borderRightWidth).toBe("0px");
  expect(styles.borderBottomWidth).toBe("0px");
  expect(styles.borderLeftWidth).toBe("0px");
  expect(styles.boxShadow).toBe("none");
});
