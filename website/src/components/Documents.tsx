import { documents, documentText } from "../content/documents";
import { DocumentList } from "./DocumentItem";
import { Section } from "./Section";

export function DesignDocuments() {
  return (
    <Section
      id="design-documents"
      heading={documentText.designHeading}
      intro={documentText.designIntro}
      tone="surface"
    >
      <DocumentList items={documents.filter((doc) => doc.category === "design-document")} />
    </Section>
  );
}

export function PosterAndPresentations() {
  return (
    <Section id="poster" heading={documentText.posterHeading} intro={documentText.posterIntro}>
      <DocumentList
        items={documents.filter(
          (doc) => doc.category === "poster" || doc.category === "presentation",
        )}
      />
    </Section>
  );
}
