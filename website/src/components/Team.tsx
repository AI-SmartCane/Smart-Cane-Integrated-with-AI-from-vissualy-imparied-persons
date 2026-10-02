import { guides, members, teamText } from "../content/team";
import type { Guide, Member } from "../content/types";
import { Portrait } from "./Portrait";
import { Section } from "./Section";

function ProfileLinks({ person }: { person: Guide | Member }) {
  if (!person.linkedin && !person.github) return null;
  return (
    <p className="mt-2 flex justify-center gap-4">
      {person.linkedin ? (
        <a href={person.linkedin} aria-label={teamText.linkedinLabel(person.name)}>
          LinkedIn
        </a>
      ) : null}
      {person.github ? (
        <a href={person.github} aria-label={teamText.githubLabel(person.name)}>
          GitHub
        </a>
      ) : null}
    </p>
  );
}

function Card({ person, lines }: { person: Guide | Member; lines: string[] }) {
  return (
    <li className="flex flex-col items-center rounded border border-line bg-canvas p-6 text-center lg:px-3">
      <Portrait photo={person.photo} name={person.name} alt={teamText.photoAlt(person.name)} />
      <h4 className="mt-4 text-xl font-bold">{person.name}</h4>
      {lines.map((line) => (
        <p key={line} className="text-base text-muted">
          {line}
        </p>
      ))}
      <ProfileLinks person={person} />
    </li>
  );
}

export function Team() {
  return (
    <Section id="team" heading={teamText.heading} tone="surface">
      <h3 className="text-2xl">{teamText.guidesHeading}</h3>
      <ul className="mt-6 grid gap-6 sm:grid-cols-2">
        {guides.map((guide) => (
          <Card
            key={guide.id}
            person={guide}
            lines={[teamText.guideRole, guide.designation, guide.organisation]}
          />
        ))}
      </ul>

      <h3 className="mt-12 text-2xl">{teamText.membersHeading}</h3>
      <ul className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {members.map((member) => (
          <Card
            key={member.id}
            person={member}
            lines={[`${teamText.usnLabel}: ${member.usn}`, member.role, member.department]}
          />
        ))}
      </ul>
    </Section>
  );
}
