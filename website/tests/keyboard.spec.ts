import { expect, test } from "@playwright/test";
import { navigation } from "../src/content/site";
import { openPage } from "./helpers";

test("desktop: first Tab reaches the skip link, then every nav link in order", async ({ page }) => {
  await openPage(page, 1280, "light");
  await page.keyboard.press("Tab");
  await expect(page.locator(":focus")).toHaveText("Skip to main content");

  for (const item of navigation) {
    await page.keyboard.press("Tab");
    await expect(page.locator(":focus")).toHaveText(item.label);
    await expect(page.locator(":focus")).toHaveAttribute("href", `#${item.target}`);
  }
  await page.keyboard.press("Tab");
  await expect(page.locator(":focus")).toHaveAccessibleName("Dark theme");
});

test("skip link moves focus to main content", async ({ page }) => {
  await openPage(page, 1280, "light");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Enter");
  await expect(page.locator("main")).toBeFocused();
});

test("mobile: menu opens, Tab reaches its links, Escape closes it and returns focus", async ({
  page,
}) => {
  await openPage(page, 375, "light");
  await page.keyboard.press("Tab");
  await expect(page.locator(":focus")).toHaveText("Skip to main content");
  await page.keyboard.press("Tab");

  const button = page.getByRole("button", { name: "Menu" });
  await expect(button).toBeFocused();
  await expect(button).toHaveAttribute("aria-expanded", "false");

  await page.keyboard.press("Enter");
  await expect(button).toHaveAttribute("aria-expanded", "true");
  const menu = page.locator(`#${await button.getAttribute("aria-controls")}`);
  await expect(menu).toBeVisible();

  for (const item of navigation) {
    await page.keyboard.press("Tab");
    await expect(page.locator(":focus")).toHaveText(item.label);
  }

  await page.keyboard.press("Escape");
  await expect(menu).toBeHidden();
  await expect(button).toHaveAttribute("aria-expanded", "false");
  await expect(button).toBeFocused();
});

test("theme toggle exposes its state and persists across reloads", async ({ page }) => {
  await openPage(page, 1280, "light");
  const toggle = page.getByRole("button", { name: "Dark theme" });
  await expect(toggle).toHaveAttribute("aria-pressed", "false");

  await toggle.press("Enter");
  await expect(toggle).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator("html")).toHaveClass(/dark/);

  await page.reload();
  await expect(page.locator("html")).toHaveClass(/dark/);
  await expect(page.getByRole("button", { name: "Dark theme" })).toHaveAttribute(
    "aria-pressed",
    "true",
  );
});

test("every interactive element shows a visible focus indicator", async ({ page }) => {
  await openPage(page, 1280, "light");
  const count = await page.locator("a:visible, button:visible").count();
  for (let i = 0; i < count; i++) {
    await page.keyboard.press("Tab");
    const outline = await page.evaluate(() => {
      const style = getComputedStyle(document.activeElement as Element);
      return { style: style.outlineStyle, width: parseFloat(style.outlineWidth) };
    });
    expect(outline.style).not.toBe("none");
    expect(outline.width).toBeGreaterThanOrEqual(2);
  }
});
