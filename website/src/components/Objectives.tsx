import { objectives } from "../content/project";
import { Section } from "./Section";

export function Objectives() {
  return (
    <Section id="objectives" heading={objectives.heading} tone="surface">
      <ol className="grid gap-6 lg:grid-cols-3">
        {objectives.items.map((item, index) => (
          <li
            key={item.title}
            className="rounded border border-line border-t-4 border-t-accent bg-canvas p-6"
          >
            <p aria-hidden="true" className="text-3xl font-bold text-accent">
              {index + 1}
            </p>
            <h3 className="mt-2 text-xl font-bold">{item.title}</h3>
            <p className="mt-3">{item.text}</p>
          </li>
        ))}
      </ol>
    </Section>
  );
}
