import { defineConfig } from "@playwright/test";

// Tests run against the production build served by `vite preview`.
// Run `npm run build` first (CI does this).
//
// Locally, PW_CHANNEL=chrome runs the tests in an installed Google Chrome instead of
// Playwright's bundled Chromium.
const channel = process.env.PW_CHANNEL;

export default defineConfig({
  testDir: "tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  // axe runs are CPU-heavy; more parallel browsers cause timeouts rather than speed-ups.
  workers: 2,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  use: {
    baseURL: "http://localhost:4173/edge-vision-guidance-cane/",
    ...(channel ? { channel } : {}),
  },
  // Screenshots are for manual review: `npm run screenshots`.
  grepInvert: process.env.SCREENSHOTS ? undefined : /@screenshots/,
  grep: process.env.SCREENSHOTS ? /@screenshots/ : undefined,
  webServer: {
    command: "npm run preview",
    url: "http://localhost:4173/edge-vision-guidance-cane/",
    reuseExistingServer: !process.env.CI,
  },
});
