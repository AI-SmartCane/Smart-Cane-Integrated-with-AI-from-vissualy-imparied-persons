import { footer } from "../content/site";

export function SiteFooter() {
  return (
    <footer className="border-t border-control bg-surface py-10 text-center text-base text-muted">
      <div className="mx-auto max-w-5xl px-4 sm:px-6">
        {footer.lines.map((line) => (
          <p key={line}>{line}</p>
        ))}
        <ul className="mt-4 flex flex-wrap justify-center gap-x-6 gap-y-2">
          {footer.links.map((link) => (
            <li key={link.target}>
              <a href={`#${link.target}`} className="inline-flex min-h-11 items-center">
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </footer>
  );
}
