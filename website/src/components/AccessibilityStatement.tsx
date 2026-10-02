import { accessibility } from "../content/accessibility";
import { Section } from "./Section";

export function AccessibilityStatement() {
  return (
    <Section id="accessibility" heading={accessibility.heading}>
      <div className="flex max-w-[70ch] flex-col gap-4">
        {accessibility.target.map((text) => (
          <p key={text}>{text}</p>
        ))}
        <h3 className="mt-4 text-2xl">{accessibility.measuresHeading}</h3>
        <ul className="list-disc pl-6">
          {accessibility.measures.map((text) => (
            <li key={text} className="mt-1">
              {text}
            </li>
          ))}
        </ul>
        <h3 className="mt-4 text-2xl">{accessibility.limitationsHeading}</h3>
        <ul className="list-disc pl-6">
          {accessibility.limitations.map((text) => (
            <li key={text} className="mt-1">
              {text}
            </li>
          ))}
        </ul>
        {accessibility.contact ? <p>{accessibility.contact}</p> : null}
      </div>
    </Section>
  );
}
