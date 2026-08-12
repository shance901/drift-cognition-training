import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";

const links = [
  { href: "#framework", label: "Framework" },
  { href: "#personas", label: "Who it's for" },
  { href: "#micro-lessons", label: "Micro-lessons" },
  { href: "#security", label: "Security" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-paper/90 backdrop-blur">
      <div className="container-page flex h-16 items-center justify-between">
        <a href="#top" className="flex items-center gap-2 text-lg font-bold text-ink" data-testid="link-home">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-iris-600 text-sm text-white">
            Y
          </span>
          <span>
            why<span className="text-iris-600">·</span>AI
          </span>
        </a>

        <nav className="hidden items-center gap-8 md:flex">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-[15px] font-medium text-ink-muted transition-colors hover:text-ink"
              data-testid={`link-nav-${link.label.toLowerCase().replace(/\s+/g, "-")}`}
            >
              {link.label}
            </a>
          ))}
        </nav>

        <div className="hidden md:block">
          <Button asChild size="sm" data-testid="button-nav-cta">
            <a href="#waitlist">Start free</a>
          </Button>
        </div>

        <button
          className="flex h-10 w-10 items-center justify-center rounded-lg text-ink md:hidden"
          onClick={() => setOpen((v) => !v)}
          aria-label={open ? "Close menu" : "Open menu"}
          data-testid="button-mobile-menu"
        >
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {open && (
        <div className="border-t border-border bg-paper md:hidden">
          <nav className="container-page flex flex-col gap-1 py-3">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className="rounded-lg px-2 py-2.5 text-[15px] font-medium text-ink-muted hover:bg-iris-50 hover:text-ink"
              >
                {link.label}
              </a>
            ))}
            <a
              href="#waitlist"
              onClick={() => setOpen(false)}
              className="mt-2 rounded-full bg-iris-600 px-4 py-2.5 text-center text-[15px] font-semibold text-white"
            >
              Start free
            </a>
          </nav>
        </div>
      )}
    </header>
  );
}
