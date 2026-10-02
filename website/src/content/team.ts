// Project guides and team members. Names, USNs, roles and departments are as in the
// legacy site's app.py.
//
// photo:    id of a processed photo (see scripts/optimize-images.mjs). Leave it out and an
//           initials avatar is shown instead.
// linkedin, github:  optional full URLs. Shown only when filled in.

import type { Guide, Member } from "./types";

export const guides: Guide[] = [
  {
    id: "k-v-suresh",
    name: "Dr. K V Suresh",
    designation: "Professor",
    organisation: "Department of ECE, SIT",
    photo: "k-v-suresh",
  },
  {
    id: "sandesh-g-v",
    name: "Sandesh G V",
    designation: "Founder / Software Developer",
    organisation: "Nasken Health, Boston, United States",
    photo: "sandesh-g-v",
    todo: "TODO: higher-resolution photo (the current one is only 200 × 200 px).",
  },
];

const department = "Electronics & Communication Engineering";

export const members: Member[] = [
  {
    id: "abhishek-kumar-singh",
    name: "Abhishek Kumar Singh",
    usn: "1SI24EC002",
    role: "Project Member",
    department,
    photo: "abhishek-kumar-singh",
  },
  {
    id: "avinash",
    name: "Avinash",
    usn: "1SI24EC017",
    role: "Project Member",
    department,
    photo: "avinash",
  },
  {
    id: "kartik-kumar-singh",
    name: "Kartik Kumar Singh",
    usn: "1SI24EC053",
    role: "Project Member",
    department,
    photo: "kartik-kumar-singh",
  },
  {
    id: "lakshisha-v-m",
    name: "Lakshisha V M",
    usn: "1SI24EC056",
    role: "Project Member",
    department,
    todo: "TODO: photo (the legacy photomini.jpg is a placeholder silhouette, not a photograph).",
  },
];

export const teamText = {
  heading: "Team",
  guidesHeading: "Project guides",
  guideRole: "Project Guide",
  membersHeading: "Team members",
  usnLabel: "USN",
  photoAlt: (name: string) => `Photo of ${name}`,
  linkedinLabel: (name: string) => `${name} on LinkedIn`,
  githubLabel: (name: string) => `${name} on GitHub`,
};
