import { components } from "../content/project";
import type { Component } from "../content/types";
import { Section } from "./Section";

function ComponentList({ items }: { items: Component[] }) {
  return (
    <ul className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {items.map((item) => (
        <li key={item.name} className="rounded border border-line bg-canvas p-5">
          <h4 className="text-xl font-bold">{item.name}</h4>
          <p className="mt-2 text-muted">{item.purpose}</p>
          {item.part ? (
            <p className="mt-2">
              <span className="font-bold">{components.partLabel}:</span> {item.part}
            </p>
          ) : null}
        </li>
      ))}
    </ul>
  );
}

export function Components() {
  return (
    <Section id="components" heading={components.heading} intro={components.intro} tone="surface">
      <h3 className="text-2xl">{components.hardwareHeading}</h3>
      <ComponentList items={components.hardware} />
      <h3 className="mt-12 text-2xl">{components.softwareHeading}</h3>
      <ComponentList items={components.software} />
    </Section>
  );
}
