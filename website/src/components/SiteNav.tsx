import { useEffect, useId, useRef, useState } from "react";
import { Menu, X } from "lucide-react";
import { navigation, ui } from "../content/site";
import { ThemeToggle } from "./ThemeToggle";

const linkClass =
  "inline-flex min-h-11 items-center rounded px-2 py-2 font-bold text-ink no-underline hover:text-accent hover:underline";

export function SiteNav() {
  const [open, setOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuId = useId();

  // Escape closes the menu and returns focus to the button.
  useEffect(() => {
    if (!open) return;
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [open]);

  return (
    <nav
      aria-label={ui.navLabel}
      className="sticky top-0 z-40 border-b border-control bg-surface [@media(max-height:30rem)]:static"
    >
      {/* DOM order: menu button, its menu, desktop links, theme toggle. The mobile menu is
          shown as a full-width row below (CSS order), but Tab reaches it straight after the
          button. */}
      <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-3 px-4 py-2 sm:px-6">
        <button
          ref={buttonRef}
          type="button"
          aria-expanded={open}
          aria-controls={menuId}
          onClick={() => setOpen((value) => !value)}
          className="inline-flex min-h-11 items-center gap-2 rounded border border-control bg-canvas px-3 py-2 text-base font-bold text-ink lg:hidden"
        >
          {open ? (
            <X aria-hidden="true" className="size-5" />
          ) : (
            <Menu aria-hidden="true" className="size-5" />
          )}
          {ui.menuButton}
        </button>

        <ul
          id={menuId}
          hidden={!open}
          className="order-last max-h-[calc(100dvh-5rem)] basis-full overflow-y-auto border-t border-line pt-2 lg:hidden"
        >
          {navigation.map((item) => (
            <li key={item.target}>
              <a
                href={`#${item.target}`}
                className={`${linkClass} w-full`}
                onClick={() => setOpen(false)}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>

        <ul className="hidden flex-wrap text-base lg:flex">
          {navigation.map((item) => (
            <li key={item.target}>
              <a href={`#${item.target}`} className={linkClass}>
                {item.label}
              </a>
            </li>
          ))}
        </ul>

        <ThemeToggle />
      </div>
    </nav>
  );
}
