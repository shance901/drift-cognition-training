import { Compass, ShieldAlert, TrendingDown } from "lucide-react";

const points = [
  {
    icon: Compass,
    title: "Curious, but overwhelmed",
    body: "Most AI education starts with a syllabus, not a person. People don't need another 40-hour course — they need a reason that's actually theirs.",
  },
  {
    icon: ShieldAlert,
    title: "Willing, but afraid",
    body: "Afraid of looking dumb in front of coworkers. Afraid of being replaced. Afraid of being scammed by the same technology they're supposed to trust.",
  },
  {
    icon: TrendingDown,
    title: "Behind, and it's expensive",
    body: "For a small business, falling behind on AI — and the cybersecurity habits that come with it — isn't just inconvenient. It's a competitive and financial risk.",
  },
];

export default function ProblemSection() {
  return (
    <section className="border-t border-border bg-surface py-20">
      <div className="container-page">
        <div className="max-w-2xl">
          <h2 className="text-balance text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            The gap isn't ability. It's fear.
          </h2>
          <p className="mt-4 text-lg text-ink-muted">
            People aren't failing to adopt AI because they can't learn it. They're stalling out because
            nobody has made it feel like it's for them.
          </p>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {points.map((point) => (
            <div key={point.title} className="rounded-2xl border border-border bg-paper p-6" data-testid={`card-problem-${point.title.toLowerCase().replace(/[^a-z]+/g, "-")}`}>
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-iris-50 text-iris-600">
                <point.icon className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-lg font-semibold text-ink">{point.title}</h3>
              <p className="mt-2 text-[15px] leading-relaxed text-ink-muted">{point.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
