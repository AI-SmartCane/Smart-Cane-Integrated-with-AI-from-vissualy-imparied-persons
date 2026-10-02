import { problem } from "../content/project";
import { Section } from "./Section";

export function Problem() {
  return (
    <Section id="problem" heading={problem.heading} tone="surface">
      <div className="flex max-w-[70ch] flex-col gap-4">
        {problem.paragraphs.map((text) => (
          <p key={text}>{text}</p>
        ))}
        <p>{problem.gapsIntro}</p>
        <ul className="list-disc pl-6">
          {problem.gaps.map((gap) => (
            <li key={gap}>{gap}</li>
          ))}
        </ul>
        <h3 className="mt-6 text-2xl">{problem.proposalHeading}</h3>
        {problem.proposal.map((text) => (
          <p key={text}>{text}</p>
        ))}
      </div>
    </Section>
  );
}
