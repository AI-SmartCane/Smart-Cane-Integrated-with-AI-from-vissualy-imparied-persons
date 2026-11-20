import type { Page } from "@playwright/test";

export const WIDTHS = [320, 375, 1280] as const;
export const THEMES = ["light", "dark"] as const;
export type Theme = (typeof THEMES)[number];

/** Opens the page in the given theme, following the OS setting (nothing stored). */
export async function openPage(page: Page, width: number, theme: Theme) {
  await page.setViewportSize({ width, height: 900 });
  await page.emulateMedia({ colorScheme: theme });
  await page.goto("./");
  await page.locator("main").waitFor();
  // Load lazy images so they are checked too.
  await page.evaluate(() => {
    for (const img of document.querySelectorAll("img")) img.loading = "eager";
  });
  await page.waitForLoadState("networkidle");
}
