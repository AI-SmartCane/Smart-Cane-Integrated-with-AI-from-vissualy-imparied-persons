import { sourceCode } from "../content/links";
import { Section } from "./Section";

export function SourceCode() {
  return (
    <Section id="source-code" heading={sourceCode.heading} intro={sourceCode.intro}>
      <ul className="flex flex-col gap-4">
        {sourceCode.links.map((link) => (
          <li key={link.href}>
            <a href={link.href} className="inline-flex min-h-11 items-center font-bold">
              {link.label}
            </a>
            {link.description ? <p className="text-muted">{link.description}</p> : null}
          </li>
        ))}
      </ul>
    </Section>
  );
}
