// Every document on the site: weekly reports, design documents, poster and presentations.
//
// To publish a document:
//   1. Put the PDF in public/docs/, e.g. public/docs/report-1-project-introduction.pdf
//   2. Change its entry below from
//        status: "planned",
//      to
//        status: "published",
//        file: "report-1-project-introduction.pdf",
//        date: "2026-10-05",          // optional, YYYY-MM-DD
//   3. Commit and push. The site rebuilds itself.

import type { ProjectDocument } from "./types";

export const documents: ProjectDocument[] = [
  // Weekly reports (shown in the Progress timeline, in this order)
  {
    id: "report-1",
    category: "weekly-report",
    title: "Report 1 — Project Introduction",
    status: "planned",
  },
  {
    id: "report-2",
    category: "weekly-report",
    title: "Report 2 — Literature Survey",
    status: "planned",
  },
  {
    id: "report-3",
    category: "weekly-report",
    title: "Report 3 — System Requirements",
    status: "planned",
  },
  {
    id: "report-4",
    category: "weekly-report",
    title: "Report 4 — Hardware Selection",
    status: "planned",
  },
  {
    id: "report-5",
    category: "weekly-report",
    title: "Report 5 — Software Development",
    status: "planned",
  },
  {
    id: "report-6",
    category: "weekly-report",
    title: "Report 6 — Prototype Development",
    status: "planned",
  },
  {
    id: "report-7",
    category: "weekly-report",
    title: "Report 7 — Testing and Validation",
    status: "planned",
  },

  // Design documents
  {
    id: "initial-design",
    category: "design-document",
    title: "Initial Design Document",
    status: "planned",
  },
  {
    id: "system-requirements",
    category: "design-document",
    title: "System Requirements Document",
    status: "planned",
  },
  {
    id: "hardware-design",
    category: "design-document",
    title: "Hardware Design Document",
    status: "planned",
  },
  {
    id: "software-design",
    category: "design-document",
    title: "Software Design Document",
    status: "planned",
  },
  {
    id: "final-design",
    category: "design-document",
    title: "Final Design Document",
    status: "planned",
  },

  // Poster and presentations
  {
    id: "poster",
    category: "poster",
    title: "Final Project Poster",
    description:
      "Will summarise the problem statement, proposed solution, system design, implementation and project results.",
    status: "planned",
  },
  {
    id: "industry-review",
    category: "presentation",
    title: "Industry Review Panel Presentation",
    description:
      "Will give an overview of the project development, system architecture, implementation and testing.",
    status: "planned",
  },
  {
    id: "faculty-presentation",
    category: "presentation",
    title: "Faculty Project Presentation",
    status: "planned",
  },
];

export const documentText = {
  progressHeading: "Progress",
  progressIntro: "Weekly reports for the 2026–27 academic year.",
  designHeading: "Design documents",
  designIntro: "Project documentation, from the first design to the final one.",
  posterHeading: "Poster and presentations",
  posterIntro: "The final poster and the presentations given to review panels.",
  published: "Published",
  planned: "Not yet published",
  publishedOn: "Published",
  /** Added to the link text of each document, by file extension. */
  formats: { pdf: "PDF", pptx: "PowerPoint", docx: "Word" } as Record<string, string>,
};
