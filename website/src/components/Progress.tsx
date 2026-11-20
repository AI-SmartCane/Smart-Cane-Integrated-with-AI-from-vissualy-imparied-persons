import { CircleCheck, Circle } from "lucide-react";
import { documents, documentText } from "../content/documents";
import { DocumentBody } from "./DocumentItem";
import { Section } from "./Section";

export function Progress() {
  const reports = documents.filter((doc) => doc.category === "weekly-report");
  return (
    <Section
      id="progress"
      heading={documentText.progressHeading}
      intro={documentText.progressIntro}
    >
      <ol className="relative flex flex-col gap-6 border-l-2 border-control pl-8">
        {reports.map((doc) => (
          <li key={doc.id} className="relative">
            <span className="absolute top-0.5 -left-[2.95rem] flex size-8 items-center justify-center rounded-full bg-canvas">
              {doc.status === "published" ? (
                <CircleCheck aria-hidden="true" className="size-7 text-accent" />
              ) : (
                <Circle aria-hidden="true" className="size-7 text-control" />
              )}
            </span>
            <DocumentBody doc={doc} />
          </li>
        ))}
      </ol>
    </Section>
  );
}
