// Turns the original team photos into small WebP files for the website.
//
// Usage:  npm run images
//
// Reads originals from  photos/originals/  (committed, so the script can be re-run)
// Writes WebP files to  src/assets/team/   plus  src/assets/team/manifest.json
//
// Every photo is cropped to the same portrait shape (4:5) and saved at 400 px and 800 px
// wide. A photo that is smaller than that is never enlarged: it is saved at its own width.
//
// To add or replace a photo: put the original in photos/originals/, add or edit its entry
// in PHOTOS below, run `npm run images`, then set `photo` for that person in
// src/content/team.ts to the same id.

import { mkdir, readdir, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const inputDir = path.join(root, "photos", "originals");
const outputDir = path.join(root, "src", "assets", "team");

/** Portrait aspect ratio used for everyone: width / height. */
const ASPECT = 4 / 5;
const WIDTHS = [400, 800];

/**
 * id:    the name used in src/content/team.ts (`photo: "<id>"`) and in the output file names.
 * file:  the original file in photos/originals/.
 * crop:  optional. The part of the original to keep, in pixels. Leave it out to crop the
 *        largest 4:5 area from the centre. When you set it, keep width / height = 4 / 5.
 */
const PHOTOS = [
  { id: "k-v-suresh", file: "Dr.-K-V-Suresh.jpg" },
  // 200 × 200 original: kept at native size (TODO: higher-resolution photo).
  { id: "sandesh-g-v", file: "sandesh_g_v.jpg" },
  // Keep the top of the photo so the head is not cut off.
  {
    id: "abhishek-kumar-singh",
    file: "photo_gtnew.jpg",
    crop: { left: 0, top: 0, width: 530, height: 662 },
  },
  // Landscape original (1296 × 972): full-height portrait crop centred on the face.
  { id: "avinash", file: "avinash.jpeg", crop: { left: 366, top: 0, width: 778, height: 972 } },
  // Wide scene: tighter crop around head and shoulders.
  {
    id: "kartik-kumar-singh",
    file: "kartik.jpeg",
    crop: { left: 160, top: 270, width: 560, height: 700 },
  },
];

function centreCrop(width, height) {
  if (width / height > ASPECT) {
    const w = Math.round(height * ASPECT);
    return { left: Math.round((width - w) / 2), top: 0, width: w, height };
  }
  const h = Math.round(width / ASPECT);
  return { left: 0, top: Math.round((height - h) / 2), width, height: h };
}

async function main() {
  await mkdir(outputDir, { recursive: true });
  for (const name of await readdir(outputDir)) {
    if (name.endsWith(".webp")) await rm(path.join(outputDir, name));
  }

  const manifest = {};
  for (const photo of PHOTOS) {
    const input = path.join(inputDir, photo.file);
    const meta = await sharp(input).metadata();
    const crop = photo.crop ?? centreCrop(meta.width, meta.height);

    if (crop.left + crop.width > meta.width || crop.top + crop.height > meta.height) {
      throw new Error(`${photo.id}: crop is outside the ${meta.width}×${meta.height} image`);
    }
    if (Math.abs(crop.width / crop.height - ASPECT) > 0.01) {
      throw new Error(`${photo.id}: crop must be 4:5 (got ${crop.width}×${crop.height})`);
    }

    // Never upscale: drop sizes wider than the cropped original.
    let widths = WIDTHS.filter((w) => w <= crop.width);
    if (widths.length === 0) widths = [crop.width];

    const sources = [];
    for (const width of widths) {
      const height = Math.round(width / ASPECT);
      const fileName = `${photo.id}-${width}.webp`;
      await sharp(input)
        .rotate()
        .extract(crop)
        .resize(width, height)
        .webp({ quality: 80 })
        .toFile(path.join(outputDir, fileName));
      sources.push({ file: fileName, width, height });
    }
    manifest[photo.id] = sources;
    console.log(`${photo.id}: ${sources.map((s) => `${s.width}×${s.height}`).join(", ")}`);
  }

  await writeFile(path.join(outputDir, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
