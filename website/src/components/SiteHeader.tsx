import { project } from "../content/project";

export function SiteHeader() {
  return (
    <header id="top" className="bg-header text-header-ink">
      <div className="mx-auto flex max-w-5xl flex-col gap-4 px-4 py-6 sm:px-6 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="text-2xl font-bold tracking-wide uppercase sm:text-3xl">
            {project.institution}
          </p>
          <p className="mt-1">
            {project.location} · Department of {project.department}
          </p>
          <p className="mt-3 max-w-[60ch] font-bold">{project.siteTitle}</p>
          <p>{project.teamLabel}</p>
        </div>
        <p className="shrink-0 text-base md:text-right">
          <span className="block font-bold">{project.departmentShort}</span>
          <span className="block italic">{project.motto}</span>
        </p>
      </div>
    </header>
  );
}
