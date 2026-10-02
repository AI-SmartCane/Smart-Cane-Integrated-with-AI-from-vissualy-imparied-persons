// Checks the built site for broken or placeholder links and images without alt text.
//
// The page is rendered by React, so this script serves dist/ with `vite preview`, opens the
// page in a headless browser and inspects the rendered HTML.
//
// Fails on:
//   - an <a> whose href is missing, empty, "#", or exactly "https://github.com/"
//   - an in-page link (#something) whose target id does not exist
//   - an <img> with no alt attribute
//   - a published document whose file is missing from public/docs/
//
// Usage: npm run build && npm run check:html

/* global document -- page.evaluate() callbacks run in the browser */

import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "@playwright/test";
import { preview } from "vite";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const BANNED = new Set(["", "#", "https://github.com/"]);

const server = await preview({ root, preview: { port: 4174, strictPort: true } });
const url = server.resolvedUrls?.local[0];
if (!url) throw new Error("vite preview did not report a URL");

// PW_CHANNEL=chrome uses an installed Google Chrome instead of Playwright's Chromium.
const browser = await chromium.launch(
  process.env.PW_CHANNEL ? { channel: process.env.PW_CHANNEL } : {},
);
const problems = [];
try {
  const page = await browser.newPage();
  await page.goto(url);
  await page.locator("main").waitFor();

  const found = await page.evaluate(() => ({
    links: [...document.querySelectorAll("a")].map((a) => ({
      href: a.getAttribute("href"),
      text: a.textContent?.trim() ?? "",
    })),
    images: [...document.querySelectorAll("img")].map((img) => ({
      src: img.getAttribute("src"),
      hasAlt: img.hasAttribute("alt"),
    })),
    ids: [...document.querySelectorAll("[id]")].map((el) => el.id),
  }));

  const ids = new Set(found.ids);
  for (const link of found.links) {
    if (link.href === null) problems.push(`Link without href: "${link.text}"`);
    else if (BANNED.has(link.href.trim()))
      problems.push(`Placeholder href "${link.href}" on link "${link.text}"`);
    else if (link.href.startsWith("#") && !ids.has(link.href.slice(1)))
      problems.push(`In-page link "${link.href}" ("${link.text}") has no matching id`);
  }
  for (const image of found.images) {
    if (!image.hasAlt) problems.push(`Image without alt: ${image.src}`);
  }

  // Node 24 (see .nvmrc) can import the TypeScript content file directly.
  const { documents } = await import(path.join(root, "src/content/documents.ts"));
  for (const doc of documents) {
    if (doc.status === "published" && !existsSync(path.join(root, "public/docs", doc.file)))
      problems.push(`Published document "${doc.title}" is missing public/docs/${doc.file}`);
  }

  console.log(`Checked ${found.links.length} links and ${found.images.length} images.`);
} finally {
  await browser.close();
  await new Promise((resolve) => server.httpServer.close(resolve));
}

if (problems.length) {
  console.error(`\n${problems.length} problem(s):\n  ${problems.join("\n  ")}`);
  process.exit(1);
}
console.log("No problems found.");
