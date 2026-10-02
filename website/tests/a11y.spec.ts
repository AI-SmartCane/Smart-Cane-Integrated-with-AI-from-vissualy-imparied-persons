import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";
import { openPage, THEMES, WIDTHS } from "./helpers";

const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"];

for (const theme of THEMES) {
  for (const width of WIDTHS) {
    test(`axe: no violations at ${width}px, ${theme}`, async ({ page }) => {
      await openPage(page, width, theme);
      const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
      expect(results.violations).toEqual([]);
    });

    test(`reflow: no horizontal scrolling at ${width}px, ${theme}`, async ({ page }) => {
      await openPage(page, width, theme);
      const fits = await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      );
      expect(fits).toBe(true);
    });
  }

  test(`axe: no violations with the mobile menu open, ${theme}`, async ({ page }) => {
    await openPage(page, 375, theme);
    await page.getByRole("button", { name: "Menu" }).click();
    const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
    expect(results.violations).toEqual([]);
  });
}

test("reflow: 200% zoom on a 1280px screen (640 CSS px)", async ({ page }) => {
  await openPage(page, 640, "light");
  const fits = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
  expect(fits).toBe(true);
});

test("page structure: one h1, no skipped heading levels, landmarks", async ({ page }) => {
  await openPage(page, 1280, "light");
  const levels = await page.evaluate(() =>
    [...document.querySelectorAll("h1, h2, h3, h4, h5, h6")].map((h) => Number(h.tagName[1])),
  );
  expect(levels.filter((level) => level === 1)).toHaveLength(1);
  expect(levels[0]).toBe(1);
  levels.forEach((level, i) => {
    if (i > 0) expect(level - (levels[i - 1] ?? 0), `heading ${i}`).toBeLessThanOrEqual(1);
  });
  for (const role of ["banner", "navigation", "main", "contentinfo"] as const) {
    await expect(page.getByRole(role)).toHaveCount(1);
  }
});

test("interactive targets are at least 24 × 24 px", async ({ page }) => {
  for (const width of [375, 1280]) {
    await openPage(page, width, "light");
    const small = await page.evaluate(() =>
      [...document.querySelectorAll("a, button")]
        .filter((el) => el.checkVisibility())
        // Links inside a sentence are exempt (WCAG 2.5.8 inline exception).
        .filter((el) => !(el.tagName === "A" && el.closest("p")))
        .map((el) => ({ text: el.textContent?.trim(), box: el.getBoundingClientRect() }))
        .filter(({ box }) => box.width < 24 || box.height < 24)
        .map(({ text, box }) => `${text} (${Math.round(box.width)}×${Math.round(box.height)})`),
    );
    expect(small, `at ${width}px`).toEqual([]);
  }
});
