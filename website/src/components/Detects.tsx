import { Armchair, BrickWall, Car, User, UtilityPole, type LucideIcon } from "lucide-react";
import { detects, type DetectIcon } from "../content/project";
import { Section } from "./Section";

const icons: Record<DetectIcon, LucideIcon> = {
  person: User,
  vehicle: Car,
  chair: Armchair,
  wall: BrickWall,
  pole: UtilityPole,
};

export function Detects() {
  return (
    <Section id="detects" heading={detects.heading} intro={detects.intro}>
      <ul className="grid grid-cols-[repeat(auto-fill,minmax(9rem,1fr))] gap-4">
        {detects.items.map((item) => {
          const Icon = icons[item.icon];
          return (
            <li
              key={item.label}
              className="flex flex-col items-center gap-3 rounded border border-line bg-surface p-5 text-center font-bold"
            >
              <Icon aria-hidden="true" className="size-9 text-accent" />
              {item.label}
            </li>
          );
        })}
      </ul>
    </Section>
  );
}
