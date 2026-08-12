import { ArrowRight, Sparkles, Flame } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function Hero() {
  return (
    <section id="top" className="relative overflow-hidden pt-16 pb-20 sm:pt-24 sm:pb-28">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -top-40 right-[-10%] h-[32rem] w-[32rem] rounded-full bg-iris-100 blur-3xl"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -bottom-32 left-[-10%] h-96 w-96 rounded-full bg-ember-100 blur-3xl"
      />

      <div className="container-page relative grid items-center gap-14 lg:grid-cols-[1.1fr_0.9fr]">
        <div>
          <Badge variant="iris" data-testid="badge-hero-eyebrow">
            <Sparkles className="h-3.5 w-3.5" />A human-centered AI framework
          </Badge>

          <h1 className="mt-6 text-balance text-4xl font-extrabold leading-[1.1] tracking-tight text-ink sm:text-5xl lg:text-6xl">
            Discover your why.
            <br />
            <span className="text-iris-600">Design your AI.</span>
          </h1>

          <p className="mt-6 max-w-xl text-lg leading-relaxed text-ink-muted">
            Most people aren't lazy about AI — they're afraid of it. This isn't another massive course.
            It's a story-first, two-minutes-a-day path that turns fear into fluency, for students, career
            switchers, later-in-life learners, and the small business owners who can't afford to fall behind.
          </p>

          <div className="mt-9 flex flex-col gap-3 sm:flex-row">
            <Button asChild size="lg" data-testid="button-hero-start">
              <a href="#waitlist">
                Start your first lesson — free
                <ArrowRight className="h-4 w-4" />
              </a>
            </Button>
            <Button asChild variant="outline" size="lg" data-testid="button-hero-how">
              <a href="#framework">See how it works</a>
            </Button>
          </div>

          <p className="mt-5 text-sm text-ink-soft">No credit card. No jargon. Just your first small win.</p>
        </div>

        <div className="relative mx-auto w-full max-w-sm">
          <div className="rounded-[2rem] border border-border bg-surface p-2 shadow-lift">
            <div className="rounded-[1.6rem] bg-gradient-to-b from-iris-600 to-iris-700 p-6 text-white">
              <div className="flex items-center justify-between text-xs font-medium text-iris-100">
                <span>Lesson 1 · Say hello to AI</span>
                <span className="flex items-center gap-1">
                  <Flame className="h-3.5 w-3.5 text-ember-300" />3
                </span>
              </div>

              <div className="mt-6 space-y-3">
                <div className="max-w-[85%] rounded-2xl rounded-tl-sm bg-white/10 px-4 py-3 text-sm">
                  Type the word <span className="font-semibold">"Hello"</span> to send your very first prompt.
                </div>
                <div className="ml-auto max-w-[70%] rounded-2xl rounded-tr-sm bg-white px-4 py-3 text-sm font-medium text-iris-700">
                  Hello
                </div>
                <div className="max-w-[90%] rounded-2xl rounded-tl-sm bg-white/10 px-4 py-3 text-sm">
                  Nice. Now finish this: <span className="font-semibold">"My name is ___ and I want to ___."</span>
                </div>
              </div>

              <div className="mt-6 flex items-center justify-between rounded-xl bg-white/10 px-4 py-3 text-xs">
                <span>Small win unlocked</span>
                <span className="font-semibold text-ember-300">+10 XP</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
