// Fails if the JavaScript loaded on first visit is over budget (gzipped).
// Counts the entry script and any modulepreload chunks referenced by dist/index.html.
//
// Usage: npm run build && npm run check:size

import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { gzipSync } from "node:zlib";

const BUDGET_KB = 120;
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const dist = path.join(root, "dist");
const html = await readFile(path.join(dist, "index.html"), "utf8");

const base = "/edge-vision-guidance-cane/";
const files = [
  ...html.matchAll(/<script[^>]+type="module"[^>]+src="([^"]+)"/g),
  ...html.matchAll(/<link[^>]+rel="modulepreload"[^>]+href="([^"]+)"/g),
].map((m) => m[1].replace(base, ""));

if (files.length === 0) throw new Error("No module scripts found in dist/index.html");

let total = 0;
for (const file of new Set(files)) {
  const size = gzipSync(await readFile(path.join(dist, file)), { level: 9 }).length;
  total += size;
  console.log(`${(size / 1000).toFixed(1).padStart(7)} KB  ${file}`);
}
console.log(
  `${(total / 1000).toFixed(1).padStart(7)} KB  total initial JS (gzipped), budget ${BUDGET_KB} KB`,
);

if (total > BUDGET_KB * 1000) {
  console.error("Initial JavaScript is over budget.");
  process.exit(1);
}
