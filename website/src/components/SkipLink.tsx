import { ui } from "../content/site";

export function SkipLink() {
  return (
    <a
      href="#main"
      className="absolute top-3 left-3 z-50 -translate-y-32 rounded bg-canvas px-4 py-3 font-bold text-accent shadow-lg focus:translate-y-0 focus-visible:outline-header-ink"
    >
      {ui.skipLink}
    </a>
  );
}
