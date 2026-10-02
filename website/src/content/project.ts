// Project identity and the descriptive sections of the page.
//
// Source: the legacy site's app.py, with the corrections listed in README.md.
// The project is in progress, so capabilities are written as design goals.

import type { Component, Paragraphs, TitledText } from "./types";

export const project = {
  siteTitle: "An Edge Vision Assistive Guidance Cane for the Visually Impaired",
  projectTitle: "Intelligent AI Stick for Visually Impaired Person",
  projectType: "Mini Project",
  academicYear: "2026–27",
  teamLabel: "Team 2026–27",
  institution: "Siddaganga Institute of Technology",
  location: "Tumakuru",
  department: "Electronics and Communication Engineering",
  departmentShort: "ECE @ SIT",
  motto: "Work is Worship",
  domain: "AI/ML/DL, Embedded Systems, IoT",
};

export const hero = {
  eyebrow: `${project.projectType} · ${project.department} · ${project.academicYear}`,
  summary:
    "A portable walking cane designed to combine a camera, a distance sensor and a Raspberry Pi 5 so that it can detect nearby objects and obstacles on the device and tell the user about them through audio and vibration feedback.",
  status:
    "This project is in progress. The features described on this page are design goals, not tested results.",
  links: [
    { label: "How it works", target: "how-it-works" },
    { label: "Meet the team", target: "team" },
  ],
};

export const problem: Paragraphs & {
  gapsIntro: string;
  gaps: string[];
  proposalHeading: string;
  proposal: string[];
} = {
  heading: "The problem",
  proposalHeading: "The proposed system",
  paragraphs: [
    "Visually impaired individuals often face difficulties while moving independently in unfamiliar indoor and outdoor environments.",
    "A conventional white cane is an important mobility aid that helps users detect obstacles through physical contact. However, it provides limited information about the objects in the surrounding environment.",
  ],
  gapsIntro: "Through contact alone, a white cane gives the user little information about:",
  gaps: ["the type of object in the way", "where the object is", "how far away the object is"],
  proposal: [
    "To address these limitations, this project proposes an Edge Vision Assistive Guidance Cane for the Visually Impaired. The proposed system integrates a camera, distance sensor, Raspberry Pi 5, computer vision, object detection and audio/vibration feedback into a portable walking cane.",
    "The Raspberry Pi 5 is designed to perform image processing and object detection locally, on the cane itself, and the system aims to identify common objects and obstacles such as people, vehicles, chairs, walls and poles.",
  ],
};

export const howItWorks = {
  heading: "How it works",
  intro: "The cane is designed to work in four stages.",
  stepsHeading: "The four stages",
  diagram: {
    title: "System diagram of the guidance cane",
    description:
      "Four stages connected by arrows, top to bottom. 1: camera and distance sensor. 2: Raspberry Pi 5 for on-device image processing, object detection and proximity estimation. 3: guidance, with avoidance instructions and spoken turn-by-turn directions. 4: audio and vibration feedback to the user. A note beside the stages says the cane keeps the normal function of a white cane.",
    boxes: [
      { title: "Camera + distance sensor", lines: ["Sense the scene ahead"] },
      { title: "Raspberry Pi 5", lines: ["On-device processing,", "object detection, proximity"] },
      { title: "Guidance", lines: ["Avoidance instructions,", "turn-by-turn directions"] },
      { title: "Audio + vibration", lines: ["Feedback to the user"] },
    ],
    caneNote: ["Still works as a", "normal white cane"],
  },
  steps: [
    {
      title: "Sense",
      text: "A camera and a distance sensor on the cane capture the scene ahead and the distance to nearby obstacles.",
    },
    {
      title: "Process on the device",
      text: "A Raspberry Pi 5 on the cane is designed to run image processing and object detection locally and to estimate how close each object is.",
    },
    {
      title: "Guide",
      text: "The system is designed to give avoidance instructions such as “Move left” or “Move right”, and spoken turn-by-turn directions when the user wishes to travel to a chosen destination.",
    },
    {
      title: "Give feedback",
      text: "Guidance reaches the user through audio and vibration feedback, while the cane keeps the normal function of a white cane.",
    },
  ] satisfies TitledText[],
};

export const objectives = {
  heading: "Objectives",
  items: [
    {
      title: "Edge-Based Perception",
      text: "To develop an edge-based perception system using a camera interfaced with a Raspberry Pi 5 that is capable of detecting and recognizing objects and obstacles in the user's surroundings in real time and estimating their proximity.",
    },
    {
      title: "Autonomous Guidance",
      text: "To enable autonomous guidance in which the system provides spoken turn-by-turn directions when the user wishes to travel to a chosen destination and provides avoidance instructions such as “Move Left / Right” to help the user steer clear of obstacles.",
    },
    {
      title: "Portable Assistive System",
      text: "To integrate environmental perception and guidance into a single portable cane prototype so that obstacle awareness and destination navigation work together through audio and vibration feedback while retaining the basic functionality of a conventional white cane.",
    },
  ] satisfies TitledText[],
};

export type DetectIcon = "person" | "vehicle" | "chair" | "wall" | "pole";

export const detects = {
  heading: "What it is designed to detect",
  intro: "The system aims to identify common objects and obstacles, including:",
  items: [
    { label: "People", icon: "person" },
    { label: "Vehicles", icon: "vehicle" },
    { label: "Chairs", icon: "chair" },
    { label: "Walls", icon: "wall" },
    { label: "Poles", icon: "pole" },
  ] satisfies { label: string; icon: DetectIcon }[],
};

export const components: {
  heading: string;
  intro: string;
  hardwareHeading: string;
  hardware: Component[];
  softwareHeading: string;
  software: Component[];
  partLabel: string;
} = {
  heading: "Hardware and software",
  intro: "The components named in the project abstract.",
  hardwareHeading: "Hardware",
  hardware: [
    {
      name: "Camera",
      purpose: "Captures the scene in front of the user.",
      todo: "TODO: camera model.",
    },
    {
      name: "Distance sensor",
      purpose: "Measures the distance to nearby obstacles.",
      todo: "TODO: distance sensor model and type.",
    },
    {
      name: "Raspberry Pi 5",
      purpose: "Runs image processing and object detection on the cane.",
      todo: "TODO: RAM variant, storage and power supply.",
    },
    {
      name: "Audio feedback",
      purpose: "Speaks guidance and directions to the user.",
      todo: "TODO: speaker or earphone part name.",
    },
    {
      name: "Vibration feedback",
      purpose: "Gives the user feedback through touch.",
      todo: "TODO: vibration motor part name.",
    },
    {
      name: "Walking cane",
      purpose: "Carries the system and keeps the normal function of a white cane.",
      todo: "TODO: cane body and battery details.",
    },
  ],
  softwareHeading: "Software",
  software: [
    {
      name: "Computer vision",
      purpose: "Image processing on the Raspberry Pi 5.",
      todo: "TODO: libraries used (name and version).",
    },
    {
      name: "Object detection",
      purpose: "Recognises objects and obstacles in the camera image.",
      todo: "TODO: detection model name and version.",
    },
    {
      name: "Proximity estimation",
      purpose: "Estimates how close each object is.",
    },
    {
      name: "Guidance",
      purpose: "Avoidance instructions and spoken turn-by-turn directions.",
      todo: "TODO: navigation and text-to-speech software.",
    },
  ],
  partLabel: "Part",
};

/** Project-level items that do not exist yet. Not shown on the page. */
export const projectTodos = [
  "TODO: test results (add a Results section once testing is done).",
  "TODO: demo video of the cane (add as a link with captions and a transcript).",
];
