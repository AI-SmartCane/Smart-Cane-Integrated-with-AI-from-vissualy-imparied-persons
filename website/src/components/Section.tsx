import type { ReactNode } from "react";

interface SectionProps {
  id: string;
  heading: string;
  intro?: string;
  /** Alternate background for visual rhythm. */
  tone?: "canvas" | "surface";
  children: ReactNode;
}

export function Section({ id, heading, intro, tone = "canvas", children }: SectionProps) {
  const headingId = `${id}-heading`;
  return (
    <section
      id={id}
      aria-labelledby={headingId}
      className={`border-t border-line py-14 sm:py-20 ${tone === "surface" ? "bg-surface" : ""}`}
    >
      <div className="mx-auto max-w-5xl px-4 sm:px-6">
        <h2 id={headingId} className="text-3xl sm:text-4xl">
          {heading}
        </h2>
        {intro ? <p className="mt-4 max-w-[70ch] text-muted">{intro}</p> : null}
        <div className="mt-8">{children}</div>
      </div>
    </section>
  );
}
