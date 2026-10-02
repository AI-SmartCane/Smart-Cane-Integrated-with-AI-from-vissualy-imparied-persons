import { Info } from "lucide-react";
import { hero, project } from "../content/project";

export function Hero() {
  const [primary, secondary] = hero.links;
  return (
    <section aria-labelledby="hero-heading" className="py-14 sm:py-20">
      <div className="mx-auto max-w-5xl px-4 sm:px-6">
        <p className="font-bold text-accent">{hero.eyebrow}</p>
        <h1 id="hero-heading" className="mt-3 max-w-[22ch] text-4xl sm:text-5xl">
          {project.siteTitle}
        </h1>
        <p className="mt-6 max-w-[62ch] text-xl">{hero.summary}</p>
        <p className="mt-6 flex max-w-[62ch] gap-3 rounded border-l-4 border-accent bg-surface p-4 text-muted">
          <Info aria-hidden="true" className="mt-1 size-5 shrink-0 text-accent" />
          {hero.status}
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          {primary ? (
            <a
              href={`#${primary.target}`}
              className="inline-flex min-h-12 items-center rounded bg-accent px-6 py-3 font-bold text-accent-ink no-underline hover:underline"
            >
              {primary.label}
            </a>
          ) : null}
          {secondary ? (
            <a
              href={`#${secondary.target}`}
              className="inline-flex min-h-12 items-center rounded border-2 border-control px-6 py-3 font-bold text-ink no-underline hover:underline"
            >
              {secondary.label}
            </a>
          ) : null}
        </div>
      </div>
    </section>
  );
}
