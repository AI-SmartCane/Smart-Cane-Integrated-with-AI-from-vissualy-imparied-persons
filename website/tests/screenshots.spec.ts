import { test } from "@playwright/test";
import { openPage, THEMES } from "./helpers";

// Full-page screenshots for manual review. Run with `npm run screenshots`.
for (const theme of THEMES) {
  for (const width of [375, 1280]) {
    test(`@screenshots ${width}px ${theme}`, async ({ page }) => {
      await openPage(page, width, theme);
      await page.screenshot({ path: `screenshots/${width}-${theme}.png`, fullPage: true });
    });
  }
}
