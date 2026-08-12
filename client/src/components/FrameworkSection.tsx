import { BookHeart, Gauge, Bot } from "lucide-react";

const steps = [
  {
    icon: BookHeart,
    step: "01",
    title: "Discover Your Why",
    body: "A short, guided conversation — not a form — uncovers your strengths, your goals, and the real reason AI should matter to you. Not in the abstract. In your life.",
  },
  {
    icon: Gauge,
    step: "02",
    title: "Assess Your Readiness",
    body: "A plain-language check across skills, tools, and basic cyber hygiene. No jargon, no judgment — just an honest starting line, wherever you're standing.",
  },
  {
    icon: Bot,
    step: "03",
    title: "Design Your AI",
    body: "Get matched with a personalized AI copilot and a learning path built from your why — delivered in small sessions you can do from your phone, anywhere.",
  },
];

export default function FrameworkSection() {
  return (
    <section id="framework" className="py-20">
      <div className="container-page">
        <div className="max-w-2xl">
          <span className="text-sm font-semibold uppercase tracking-wide text-iris-600">The framework</span>
          <h2 className="mt-3 text-balance text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Discover your why. Design your AI.
          </h2>
          <p className="mt-4 text-lg text-ink-muted">
            A human-centered path from "I'm not sure this is for me" to "I have an AI copilot built around
            how I actually think and work."
          </p>
        </div>

        <div className="relative mt-14 grid gap-8 lg:grid-cols-3">
          <div aria-hidden="true" className="absolute left-0 right-0 top-[3.25rem] hidden h-px bg-border lg:block" />

          {steps.map((step) => (
            <div key={step.title} className="relative" data-testid={`card-framework-step-${step.step}`}>
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl border-4 border-paper bg-iris-600 text-white shadow-soft">
                <step.icon className="h-7 w-7" />
              </div>
              <div className="mt-5 text-sm font-bold text-iris-500">Step {step.step}</div>
              <h3 className="mt-1 text-xl font-bold text-ink">{step.title}</h3>
              <p className="mt-2 text-[15px] leading-relaxed text-ink-muted">{step.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
