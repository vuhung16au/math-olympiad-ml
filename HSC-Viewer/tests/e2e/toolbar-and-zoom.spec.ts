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

test("icon-only share buttons trigger Facebook popup, native share for Instagram/TikTok, Discord, and copy link", async ({ page }) => {
  await gotoViewer(page, { mockMode: "success" });

  await page.evaluate(() => {
    (window as Window & { __openCalls?: unknown[][] }).__openCalls = [];
    (window as Window & { __shareCalls?: unknown[] }).__shareCalls = [];
    (window as Window & { __copiedText?: string }).__copiedText = "";

    window.open = (...args: unknown[]) => {
      const win = window as Window & { __openCalls: unknown[][] };
      win.__openCalls.push(args);
      return null;
    };

    Object.defineProperty(navigator, "share", {
      configurable: true,
      value: async (payload: unknown) => {
        const win = window as Window & { __shareCalls: unknown[] };
        win.__shareCalls.push(payload);
      },
    });

    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: {
        writeText: async (text: string) => {
          const win = window as Window & { __copiedText: string };
          win.__copiedText = text;
        },
      },
    });
  });

  const facebookButton = page.getByRole("button", { name: "Facebook" });
  const instagramButton = page.getByRole("button", { name: "Instagram" });
  const discordButton = page.getByRole("button", { name: "Discord" });
  const tiktokButton = page.getByRole("button", { name: "TikTok" });
  const copyLinkButton = page.getByRole("button", { name: "Copy link" });

  await expect(facebookButton).toBeVisible();
  await expect(instagramButton).toBeVisible();
  await expect(discordButton).toBeVisible();
  await expect(tiktokButton).toBeVisible();
  await expect(copyLinkButton).toBeVisible();

  // Buttons are icon-only in the toolbar; names exist in aria labels, not visible text.
  await expect(page.getByText("Facebook", { exact: true })).toHaveCount(0);
  await expect(page.getByText("Instagram", { exact: true })).toHaveCount(0);
  await expect(page.getByText("Discord", { exact: true })).toHaveCount(0);
  await expect(page.getByText("TikTok", { exact: true })).toHaveCount(0);
  await expect(page.getByText("Copy link", { exact: true })).toHaveCount(0);

  await facebookButton.click();

  const facebookOpenUrl = await page.evaluate(() => {
    const win = window as Window & { __openCalls: unknown[][] };
    const lastCall = win.__openCalls.at(-1);
    return typeof lastCall?.[0] === "string" ? lastCall[0] : "";
  });

  const facebookParsed = new URL(facebookOpenUrl);
  expect(facebookParsed.origin).toBe("https://www.facebook.com");
  expect(facebookParsed.pathname).toBe("/sharer/sharer.php");
  expect(facebookParsed.searchParams.get("u")).toBe("http://localhost:3000/booklets/hsc-collections/1");
  expect(facebookParsed.searchParams.get("quote")).toContain("Check out this awesome HSC math booklet on HSC Collections");

  await instagramButton.click();
  await discordButton.click();
  await tiktokButton.click();

  const discordOpenUrl = await page.evaluate(() => {
    const win = window as Window & { __openCalls: unknown[][] };
    // Discord is opened as the second last call (after other buttons)
    const calls = win.__openCalls;
    const discordCall = calls.find((call) => typeof call?.[0] === "string" && call[0].includes("discord.gg"));
    return typeof discordCall?.[0] === "string" ? discordCall[0] : "";
  });

  expect(discordOpenUrl).toBe("https://discord.gg/MPT3FFkg");

  const shareCalls = await page.evaluate(() => {
    const win = window as Window & { __shareCalls: unknown[] };
    return win.__shareCalls as Array<{ title: string; text: string; url: string }>;
  });

  expect(shareCalls).toHaveLength(2);
  for (const payload of shareCalls) {
    expect(payload.title).toBe("HSC Collections - HSC Maths Booklet");
    expect(payload.text).toContain("Check out this awesome HSC math booklet on HSC Collections");
    expect(payload.url).toBe("http://localhost:3000/booklets/hsc-collections/1");
  }

  await copyLinkButton.click();
  await expect(page.getByText("Link copied to clipboard!")).toBeVisible();

  const copiedText = await page.evaluate(() => {
    const win = window as Window & { __copiedText: string };
    return win.__copiedText;
  });
  expect(copiedText).toBe("http://localhost:3000/booklets/hsc-collections/1");
});
