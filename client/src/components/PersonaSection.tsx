import { GraduationCap, Briefcase, Heart, Building2 } from "lucide-react";

const personas = [
  {
    icon: GraduationCap,
    title: "High schoolers",
    tag: "Get ahead, not left behind",
    body: "Walk into college and your first job already fluent — not just someone who uses a chatbot, but someone who knows how to think alongside one.",
  },
  {
    icon: Briefcase,
    title: "Career changers & mid-career pros",
    tag: "Stay indispensable",
    body: "Learn to lead with AI before your role changes without you. Small sessions that fit around a full-time job, not instead of one.",
  },
  {
    icon: Heart,
    title: "Later-in-life learners",
    tag: "No jargon, no judgment",
    body: "Built for people who've never trusted a chatbot with anything important — plain language, real pacing, and zero condescension.",
  },
  {
    icon: Building2,
    title: "Small & medium business owners",
    tag: "Compete and protect",
    body: "Your competitors are already automating. Learn to use AI to grow — and pick up the cybersecurity habits that keep your business safe while you do it.",
  },
];

export default function PersonaSection() {
  return (
    <section id="personas" className="border-t border-border bg-surface py-20">
      <div className="container-page">
        <div className="max-w-2xl">
          <span className="text-sm font-semibold uppercase tracking-wide text-iris-600">Who it's for</span>
          <h2 className="mt-3 text-balance text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Built for the whole room, not just the front row.
          </h2>
          <p className="mt-4 text-lg text-ink-muted">
            One framework. Four very different starting points. Every path begins with the same question:
            what's your why?
          </p>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2">
          {personas.map((persona) => (
            <div
              key={persona.title}
              className="flex gap-4 rounded-2xl border border-border bg-paper p-6"
              data-testid={`card-persona-${persona.title.toLowerCase().replace(/[^a-z]+/g, "-")}`}
            >
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-ember-50 text-ember-600">
                <persona.icon className="h-6 w-6" />
              </div>
              <div>
                <div className="text-xs font-semibold uppercase tracking-wide text-ember-600">{persona.tag}</div>
                <h3 className="mt-1 text-lg font-semibold text-ink">{persona.title}</h3>
                <p className="mt-2 text-[15px] leading-relaxed text-ink-muted">{persona.body}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
