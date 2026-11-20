import { projectInfo, ui } from "../content/site";
import { Section } from "./Section";

export function ProjectInfo() {
  return (
    <Section id="project-information" heading={ui.projectInfoHeading} tone="surface">
      <dl className="grid max-w-3xl gap-x-8 gap-y-3 rounded border-l-4 border-accent bg-canvas p-6 sm:grid-cols-[auto_1fr]">
        {projectInfo.map((row) => (
          <div key={row.label} className="contents">
            <dt className="font-bold">{row.label}</dt>
            <dd className="mb-2 sm:mb-0">{row.value}</dd>
          </div>
        ))}
      </dl>
    </Section>
  );
}
