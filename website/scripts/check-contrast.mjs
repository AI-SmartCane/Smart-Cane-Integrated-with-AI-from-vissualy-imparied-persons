// Checks WCAG contrast for every colour pairing the site uses, in both themes.
// Reads the colour tokens from src/index.css.
//
// Usage: npm run check:contrast

import { readFile } from "node:fs/promises";

const css = await readFile(new URL("../src/index.css", import.meta.url), "utf8");

function tokens(selector) {
  const start = css.indexOf(`${selector} {`);
  if (start === -1) throw new Error(`No "${selector}" block in src/index.css`);
  const block = css.slice(start, css.indexOf("}", start));
  return Object.fromEntries(
    [...block.matchAll(/--([a-z-]+):\s*(#[0-9a-f]{6})/gi)].map((m) => [m[1], m[2].toLowerCase()]),
  );
}

function luminance(hex) {
  const [r, g, b] = [1, 3, 5].map((i) => {
    const c = parseInt(hex.slice(i, i + 2), 16) / 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function ratio(a, b) {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

// [foreground, background, minimum ratio, what it is]
const PAIRS = [
  ["ink", "canvas", 4.5, "body text"],
  ["ink", "surface", 4.5, "text on panels"],
  ["muted", "canvas", 4.5, "secondary text"],
  ["muted", "surface", 4.5, "secondary text on panels"],
  ["accent", "canvas", 4.5, "links and accent text"],
  ["accent", "surface", 4.5, "links on panels"],
  ["accent-ink", "accent", 4.5, "button text"],
  ["header-ink", "header", 4.5, "header text"],
  ["focus", "canvas", 3, "focus indicator"],
  ["focus", "surface", 3, "focus indicator on panels"],
  ["control", "canvas", 3, "control borders"],
  ["control", "surface", 3, "control borders on panels"],
  ["accent", "canvas", 3, "accent UI (timeline, borders)"],
  ["accent", "surface", 3, "accent UI on panels"],
  // The header holds no links or buttons. The only focus ring drawn over it is the skip link's.
  ["focus", "header", 3, "default focus ring next to the header"],
  ["header-ink", "header", 3, "skip link focus ring over the header"],
];

let failed = false;

// The no-JavaScript dark theme (prefers-color-scheme block) must match the toggled one.
const toggled = tokens(":root.dark");
const system = tokens(":root:not(.light):not(.dark)");
for (const name of new Set([...Object.keys(toggled), ...Object.keys(system)])) {
  if (toggled[name] !== system[name]) {
    failed = true;
    console.log(
      `FAIL  --${name}: :root.dark ${toggled[name]} vs prefers-color-scheme ${system[name]}`,
    );
  }
}

for (const [theme, selector] of [
  ["light", ":root"],
  ["dark", ":root.dark"],
]) {
  const t = tokens(selector);
  console.log(`\n${theme}`);
  for (const [fg, bg, min, what] of PAIRS) {
    const r = ratio(t[fg], t[bg]);
    const ok = r >= min;
    if (!ok) failed = true;
    console.log(
      `  ${ok ? "pass" : "FAIL"}  ${r.toFixed(2).padStart(5)}:1 (min ${min})  ${fg} on ${bg}  — ${what}`,
    );
  }
}

if (failed) {
  console.error("\nContrast check failed.");
  process.exit(1);
}
console.log("\nAll pairings pass.");
