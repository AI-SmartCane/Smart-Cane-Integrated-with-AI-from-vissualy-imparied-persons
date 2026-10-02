import { howItWorks } from "../content/project";
import { Section } from "./Section";
import { SystemDiagram } from "./SystemDiagram";

export function HowItWorks() {
  return (
    <Section id="how-it-works" heading={howItWorks.heading} intro={howItWorks.intro}>
      <div className="grid items-start gap-10 md:grid-cols-2">
        <div>
          <h3 className="text-2xl">{howItWorks.stepsHeading}</h3>
          <ol className="mt-6 flex flex-col gap-6">
            {howItWorks.steps.map((step, index) => (
              <li key={step.title} className="flex gap-4">
                <span
                  aria-hidden="true"
                  className="flex size-9 shrink-0 items-center justify-center rounded-full bg-accent font-bold text-accent-ink"
                >
                  {index + 1}
                </span>
                <div>
                  <h4 className="text-xl font-bold">{step.title}</h4>
                  <p className="mt-1 max-w-[60ch]">{step.text}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>
        <SystemDiagram />
      </div>
    </Section>
  );
}
