// Navigation, interface labels and footer text.

import type { NavItem } from "./types";
import { project } from "./project";

export const navigation: NavItem[] = [
  { label: "The problem", target: "problem" },
  { label: "How it works", target: "how-it-works" },
  { label: "Objectives", target: "objectives" },
  { label: "Components", target: "components" },
  { label: "Progress", target: "progress" },
  { label: "Documents", target: "design-documents" },
  { label: "Team", target: "team" },
  { label: "Source code", target: "source-code" },
];

export const ui = {
  skipLink: "Skip to main content",
  navLabel: "Sections",
  menuButton: "Menu",
  darkTheme: "Dark theme",
  projectInfoHeading: "Project information",
};

export const projectInfo = [
  { label: "Institution", value: `${project.institution}, ${project.location}` },
  { label: "Department", value: project.department },
  { label: "Project title", value: project.projectTitle },
  { label: "Project type", value: project.projectType },
  { label: "Academic year", value: project.academicYear },
  { label: "Domain", value: project.domain },
];

export const footer = {
  lines: [
    project.projectType,
    `Department of ${project.department}`,
    `${project.institution}, ${project.location}`,
    `Academic Year ${project.academicYear}`,
  ],
  links: [
    { label: "Accessibility", target: "accessibility" },
    { label: "Back to top", target: "top" },
  ],
};
