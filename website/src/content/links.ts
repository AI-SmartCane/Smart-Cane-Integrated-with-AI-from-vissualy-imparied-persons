// Source code links.

import type { ExternalLink } from "./types";

export const sourceCode: {
  heading: string;
  intro: string;
  links: ExternalLink[];
  todo: string;
} = {
  heading: "Source code",
  intro:
    "The code for this website is on GitHub, under the NaskenAI organisation. A link to the cane's own software will be added here when it is published.",
  links: [
    {
      label: "NaskenAI on GitHub",
      href: "https://github.com/NaskenAI",
      description: "The GitHub organisation.",
    },
    {
      label: "Website source",
      href: "https://github.com/NaskenAI/edge-vision-guidance-cane",
      description: "The code for this website.",
    },
  ],
  todo: "TODO: link to the cane's own software repository once it exists.",
};
