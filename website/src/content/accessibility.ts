// Accessibility statement.

export const accessibility: {
  heading: string;
  target: string[];
  measuresHeading: string;
  measures: string[];
  limitationsHeading: string;
  limitations: string[];
  /** Contact line. Hidden until an email address is supplied. */
  contact?: string;
  todo: string;
} = {
  heading: "Accessibility",
  target: [
    "This project is about visual impairment, so accessibility is the main quality bar for this website. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA.",
  ],
  measuresHeading: "What we do",
  measures: [
    "Use the Atkinson Hyperlegible typeface, designed for low-vision readers, at a comfortable size.",
    "Provide a text version of every diagram and descriptive text for every photo.",
    "Support full keyboard use, browser zoom up to 400% (content reflows at 320 px width without sideways scrolling), and light and dark themes.",
    "Test every change automatically with axe in both themes, at phone and desktop widths.",
  ],
  limitationsHeading: "Known limitations",
  limitations: [
    "Automated tests find only some accessibility problems. The site has not yet been reviewed by screen reader or magnifier users.",
    "Reports and other documents will be PDF files, which are not covered by the automated tests.",
    "There is no contact address for accessibility feedback yet.",
  ],
  todo: "TODO: add an accessibility contact email (set `contact`) and remove the last limitation.",
};
