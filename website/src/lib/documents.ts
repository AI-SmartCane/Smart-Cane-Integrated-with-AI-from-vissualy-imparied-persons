import { documentText } from "../content/documents";

export function formatLabel(file: string) {
  const extension = file.split(".").pop()?.toLowerCase() ?? "";
  return documentText.formats[extension] ?? extension.toUpperCase();
}

export function formatDate(date: string) {
  return new Intl.DateTimeFormat("en-GB", { dateStyle: "long", timeZone: "UTC" }).format(
    new Date(`${date}T00:00:00Z`),
  );
}

export function documentHref(file: string) {
  return `${import.meta.env.BASE_URL}docs/${file}`;
}
