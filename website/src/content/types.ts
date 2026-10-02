// Shared types for everything in src/content/.
//
// `todo` fields are notes for the team. They are never shown on the website.

export type DocumentCategory = "weekly-report" | "design-document" | "poster" | "presentation";

interface DocumentBase {
  /** Short unique id, e.g. "report-1". */
  id: string;
  /** Shown on the page. The file format is added automatically, e.g. "(PDF)". */
  title: string;
  category: DocumentCategory;
  /** Optional one-line description shown under the title. */
  description?: string;
  /** Optional publication date in YYYY-MM-DD format, e.g. "2026-10-05". */
  date?: string;
  todo?: string;
}

export interface PublishedDocument extends DocumentBase {
  status: "published";
  /** File name inside public/docs/, e.g. "report-1-project-introduction.pdf". */
  file: string;
}

export interface PlannedDocument extends DocumentBase {
  status: "planned";
  file?: never;
}

export type ProjectDocument = PublishedDocument | PlannedDocument;

/** Id of a processed photo in src/assets/team/manifest.json (see scripts/optimize-images.mjs). */
export type PhotoId = string;

interface PersonBase {
  id: string;
  name: string;
  /** Leave out when there is no photo; an initials avatar is shown instead. */
  photo?: PhotoId;
  linkedin?: string;
  github?: string;
  todo?: string;
}

export interface Guide extends PersonBase {
  designation: string;
  organisation: string;
}

export interface Member extends PersonBase {
  usn: string;
  role: string;
  department: string;
}

export interface NavItem {
  label: string;
  /** Id of the section to jump to, without "#". */
  target: string;
}

export interface Paragraphs {
  heading: string;
  paragraphs: string[];
}

export interface TitledText {
  title: string;
  text: string;
}

export interface Component {
  name: string;
  purpose: string;
  /** Specific model or part name. Hidden until filled in. */
  part?: string;
  todo?: string;
}

export interface ExternalLink {
  label: string;
  href: string;
  description?: string;
}
