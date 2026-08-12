import { ShieldCheck, KeyRound, Fingerprint, MailWarning } from "lucide-react";

const habits = [
  {
    icon: MailWarning,
    title: "Spot AI-powered scams",
    body: "Phishing and deepfake attempts are getting harder to catch. Every path includes plain-language lessons on what to watch for.",
  },
  {
    icon: KeyRound,
    title: "Lock down the basics",
    body: "Passwords, multi-factor authentication, and safe device habits — the unglamorous fundamentals that stop most breaches.",
  },
  {
    icon: Fingerprint,
    title: "Use AI tools safely",
    body: "What's okay to paste into a chatbot and what isn't — especially when customer or business data is involved.",
  },
];

export default function SecuritySection() {
  return (
    <section id="security" className="border-t border-border bg-surface py-20">
      <div className="container-page grid gap-12 lg:grid-cols-[0.8fr_1.2fr] lg:items-center">
        <div>
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-iris-600 text-white">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <h2 className="mt-5 text-balance text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            AI readiness includes cyber resilience.
          </h2>
          <p className="mt-4 text-lg text-ink-muted">
            You can't fully embrace AI without also learning to protect yourself from what it makes
            possible. That's especially true for small business owners, whose entire livelihood can hinge
            on one bad click. So security isn't a separate course — it's baked into the same small lessons.
          </p>
        </div>

        <div className="grid gap-6 sm:grid-cols-3">
          {habits.map((habit) => (
            <div
              key={habit.title}
              className="rounded-2xl border border-border bg-paper p-6"
              data-testid={`card-security-${habit.title.toLowerCase().replace(/[^a-z]+/g, "-")}`}
            >
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-iris-50 text-iris-600">
                <habit.icon className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-semibold text-ink">{habit.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-ink-muted">{habit.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
