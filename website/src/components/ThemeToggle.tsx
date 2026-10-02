import { useState } from "react";
import { Moon, Sun } from "lucide-react";
import { ui } from "../content/site";

const STORAGE_KEY = "theme";

/** index.html applies a saved theme before the first paint; otherwise follow the OS setting. */
function isDarkNow() {
  const root = document.documentElement;
  if (root.classList.contains("dark")) return true;
  if (root.classList.contains("light")) return false;
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function applyTheme(dark: boolean) {
  const root = document.documentElement;
  root.classList.toggle("dark", dark);
  root.classList.toggle("light", !dark);
  try {
    localStorage.setItem(STORAGE_KEY, dark ? "dark" : "light");
  } catch {
    // Storage can be unavailable (private browsing). The theme still changes for this visit.
  }
}

export function ThemeToggle() {
  const [dark, setDark] = useState(isDarkNow);

  return (
    <button
      type="button"
      aria-pressed={dark}
      onClick={() => {
        applyTheme(!dark);
        setDark(!dark);
      }}
      className="inline-flex min-h-11 shrink-0 items-center gap-2 rounded border border-control bg-canvas px-3 py-2 text-base font-bold text-ink"
    >
      {dark ? (
        <Moon aria-hidden="true" className="size-5" />
      ) : (
        <Sun aria-hidden="true" className="size-5" />
      )}
      {ui.darkTheme}
    </button>
  );
}
