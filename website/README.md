# An Edge Vision Assistive Guidance Cane for the Visually Impaired

Project website for a Mini Project in the Department of Electronics and Communication
Engineering, Siddaganga Institute of Technology, Tumakuru (Team 2026–27).

**Live site:** https://naskenai.github.io/edge-vision-guidance-cane/

The cane is designed to use a camera, a distance sensor and a Raspberry Pi 5 to detect
obstacles on the device and guide the user through audio and vibration feedback. This
repository holds only the **website**. The cane's own software will live in a separate
repository.

Because the project is about visual impairment, accessibility is the main quality bar for this
site. Every change is checked automatically (see [Checks](#checks)).

## What it is built with

- [Vite](https://vite.dev/) + [React](https://react.dev/) + TypeScript (strict mode)
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Atkinson Hyperlegible](https://fontsource.org/fonts/atkinson-hyperlegible), self-hosted
- Hosted on GitHub Pages. No backend, analytics, cookies or trackers.

You do **not** need to know React to update the site. Almost everything you will change is
in `src/content/`.

## Run it on your computer

You need [Node.js](https://nodejs.org/) 24 (the version is in `.nvmrc`) and Git.

```sh
git clone https://github.com/NaskenAI/edge-vision-guidance-cane.git
cd edge-vision-guidance-cane
npm ci          # install exactly the versions in package-lock.json
npm run dev     # start a local copy of the site
```

Open the address it prints (usually http://localhost:5173/edge-vision-guidance-cane/). The
page reloads automatically when you save a file.

## Where things are

| What                                     | Where                      |
| ---------------------------------------- | -------------------------- |
| All text on the page                     | `src/content/*.ts`         |
| Weekly reports, design documents, etc.   | `src/content/documents.ts` |
| PDF files                                | `public/docs/`             |
| Guides and team members                  | `src/content/team.ts`      |
| Original team photos                     | `photos/originals/`        |
| Processed photos (generated, don't edit) | `src/assets/team/`         |
| Page layout and components               | `src/components/`          |
| Colours                                  | `src/index.css`            |

## Common tasks

### Publish a weekly report

1. Export the report as a PDF. Please use your word processor's "tagged PDF" or
   "accessible PDF" option if it has one.
2. Give it a short name with no spaces, e.g. `report-1-project-introduction.pdf`, and put it
   in `public/docs/`.
3. Open `src/content/documents.ts` and find the report's entry:

   ```ts
   {
     id: "report-1",
     category: "weekly-report",
     title: "Report 1 — Project Introduction",
     status: "planned",
   },
   ```

4. Change `status` to `"published"` and add the file name (and, if you like, the date):

   ```ts
   {
     id: "report-1",
     category: "weekly-report",
     title: "Report 1 — Project Introduction",
     status: "published",
     file: "report-1-project-introduction.pdf",
     date: "2026-10-05",
   },
   ```

5. Run `npm run dev` and check that the link works. The site adds "(PDF)" to the link text
   for you.
6. Commit both files and push (or open a pull request). The live site updates within a few
   minutes.

If you mark a document `published` but forget the PDF, the checks fail and tell you which
file is missing.

### Add or publish a design document, poster or presentation

The same steps as a weekly report. These live in the same file, `src/content/documents.ts`,
under the "Design documents" and "Poster and presentations" comments. To add a new one, copy
an existing entry, give it a new unique `id`, and set `category` to one of
`"design-document"`, `"poster"` or `"presentation"`.

### Update a team member's details

Edit `src/content/team.ts`. Each person has a name, USN, role and department. Two fields are
optional and are only shown when filled in:

```ts
linkedin: "https://www.linkedin.com/in/your-profile/",
github: "https://github.com/your-username",
```

### Add or replace a photo

1. Put the original photo (JPEG or PNG) in `photos/originals/`. Please use a photo at least
   400 px wide, ideally 800 px or more.
2. Open `scripts/optimize-images.mjs` and add or edit the person's line in `PHOTOS`:

   ```js
   { id: "lakshisha-v-m", file: "lakshisha.jpg" },
   ```

   Without `crop`, the script cuts the largest 4:5 portrait from the centre. If the face ends
   up off-centre, add a `crop` with pixel values (it must stay 4:5, e.g. 640 × 800).

3. Run:

   ```sh
   npm run images
   ```

   This writes WebP files at 400 px and 800 px wide into `src/assets/team/`. It never
   enlarges a small photo.

4. In `src/content/team.ts`, set the person's `photo` to the same id:
   `photo: "lakshisha-v-m",`
5. Run `npm run dev`, look at the photo, then commit `photos/originals/`, `src/assets/team/`,
   the script and `team.ts`.

Anyone without a `photo` is shown with their initials instead.

## Checks

Run these before you push. CI runs all of them on every push and pull request.

```sh
npm run typecheck      # TypeScript errors
npm run lint           # code and accessibility lint rules
npm run format:check   # formatting (fix it with: npm run format)
npm run check:contrast # colour contrast for every colour pairing, both themes
npm run build          # build the site into dist/
npm run check:size     # first-load JavaScript must stay under 120 KB (gzipped)
npm run check:html     # no placeholder links (#, empty, bare github.com), every image has alt text
npm run test:e2e       # axe accessibility, keyboard, zoom/reflow tests
```

The browser tests need Playwright's browser once: `npx playwright install chromium`. If that
download fails on your network, run the tests in your installed Google Chrome instead:
`PW_CHANNEL=chrome npm run test:e2e` (and the same for `check:html`).

`npm run screenshots` saves full-page screenshots at 375 px and 1280 px, in both themes,
to `screenshots/` for you to look over.

**Do not switch off a lint rule or weaken a test to get a pass.** Fix the page instead. If
you're stuck, ask a guide.

## How deployment works

- `.github/workflows/ci.yml` runs every check above on every push and pull request.
- `.github/workflows/deploy.yml` runs on every push to `main`. It builds the site and
  publishes `dist/` to GitHub Pages.

### Reading a failed run

1. On GitHub, open the **Actions** tab, or click the red ✗ next to your commit.
2. Open the failed run and click the job name (**checks** or **build**).
3. Find the first step with a red ✗ and expand it. The error is usually in the last
   20 lines.
4. What the step names mean:
   - **Type check**: a TypeScript error, often a typo in `src/content/`, e.g. a missing
     comma or quote, or a field with the wrong name.
   - **Lint**: a code or accessibility rule, e.g. an image without `alt`.
   - **Formatting**: run `npm run format` and commit the result.
   - **Links and image alt text**: a link to `#` or a missing PDF. The message names it.
   - **Accessibility (axe) and keyboard tests**: download the `playwright-report` file at the
     bottom of the run page, unzip it, and open `index.html` to see exactly what failed.
5. Fix it on your computer, run the same command locally until it passes, and push again.

## Corrections made to the legacy Streamlit site

This site replaces an earlier Streamlit (Python) version. Its content was carried over with
these corrections:

1. Motto "WORK IS WORKSHIP" → "Work is Worship".
2. Removed a stray "-----" before "Team 2026-27".
3. Removed text left over from another project's template ("the First Responder Drone
   project").
4. The two GitHub links pointed to https://github.com/ itself. They now point to the NaskenAI
   organisation and to this website's repository.
5. All 15 document links pointed to `#`. Documents are now listed with a status, and
   unpublished ones say "Not yet published" instead of linking nowhere.
6. The site used three names for the project. The page title is now "An Edge Vision
   Assistive Guidance Cane for the Visually Impaired". "Intelligent AI Stick for Visually
   Impaired Person" appears once, as the project title in Project information.
7. Academic year is "2026–27" and project type is "Mini Project" everywhere.
8. Guide 2's affiliation is "Founder / Software Developer, Nasken Health, Boston, United
   States".
9. The placeholder silhouette photo for Lakshisha V M was removed; initials are shown until
   a real photo is supplied.

The abstract described a proposed system, so the site describes capabilities as design goals
("is designed to", "aims to"), not results.

## Open TODOs

Each of these is also recorded as a `todo` field in `src/content/` and is **not** shown on
the site.

**Documents:** all 15 PDFs (7 weekly reports, 5 design documents, the poster, and the industry
review and faculty presentations).

**Team:**

- Photo for Lakshisha V M.
- Higher-resolution photo of Sandesh G V (the current one is 200 × 200 px).
- LinkedIn and GitHub links for anyone who wants them shown.

**Hardware and software details** (`src/content/project.ts`):

- Camera model.
- Distance sensor model and type.
- Raspberry Pi 5 RAM variant, storage and power supply.
- Speaker or earphone part name.
- Vibration motor part name.
- Cane body and battery details.
- Computer vision libraries (name and version).
- Detection model name and version.
- Navigation and text-to-speech software.

**Other:**

- Test results (add a Results section once testing is done).
- Demo video of the cane (with captions and a transcript).
- Link to the cane's own software repository (`src/content/links.ts`).
- Accessibility contact email (`src/content/accessibility.ts`). When it's added, remove the
  "no contact address" limitation.

## Open decisions

- **Licence:** no licence file has been added yet. Until one is chosen, the code is "all
  rights reserved" by default. The team and guides should pick one (for example MIT for the
  code and CC BY 4.0 for the documents).
