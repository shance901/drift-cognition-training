export default function Footer() {
  return (
    <footer className="border-t border-border py-10">
      <div className="container-page flex flex-col items-start justify-between gap-6 sm:flex-row sm:items-center">
        <div>
          <div className="flex items-center gap-2 text-base font-bold text-ink">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-iris-600 text-xs text-white">
              Y
            </span>
            why<span className="text-iris-600">·</span>AI
          </div>
          <p className="mt-2 max-w-sm text-sm text-ink-soft">
            Discover your why. Design your AI. A human-centered path to AI fluency, one small win at a time.
          </p>
        </div>

        <nav className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-ink-muted">
          <a href="#framework" className="hover:text-ink">Framework</a>
          <a href="#personas" className="hover:text-ink">Who it's for</a>
          <a href="#micro-lessons" className="hover:text-ink">Micro-lessons</a>
          <a href="#security" className="hover:text-ink">Security</a>
        </nav>
      </div>

      <div className="container-page mt-8 border-t border-border pt-6 text-xs text-ink-soft">
        © {new Date().getFullYear()} why·AI. Built to help everyone reach their fullest potential.
      </div>
    </footer>
  );
}
