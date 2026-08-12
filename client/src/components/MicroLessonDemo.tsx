import { useState, type FormEvent } from "react";
import { Flame, Sparkles, ArrowRight, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type Step = "intro" | "hello" | "why" | "done";

const XP_PER_STEP = { hello: 10, why: 15 } as const;

export default function MicroLessonDemo() {
  const [step, setStep] = useState<Step>("intro");
  const [helloText, setHelloText] = useState("");
  const [whyText, setWhyText] = useState("");
  const [xp, setXp] = useState(0);

  function submitHello(e: FormEvent) {
    e.preventDefault();
    if (!helloText.trim()) return;
    setXp((v) => v + XP_PER_STEP.hello);
    setStep("why");
  }

  function submitWhy(e: FormEvent) {
    e.preventDefault();
    if (!whyText.trim()) return;
    setXp((v) => v + XP_PER_STEP.why);
    setStep("done");
  }

  function reset() {
    setStep("intro");
    setHelloText("");
    setWhyText("");
    setXp(0);
  }

  return (
    <section id="micro-lessons" className="py-20">
      <div className="container-page grid items-start gap-14 lg:grid-cols-[0.9fr_1.1fr]">
        <div>
          <span className="text-sm font-semibold uppercase tracking-wide text-iris-600">Small wins, on repeat</span>
          <h2 className="mt-3 text-balance text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Two minutes a day beats a course you'll never finish.
          </h2>
          <p className="mt-4 text-lg text-ink-muted">
            The same mechanics that make language apps genuinely stick — tiny sessions, instant feedback,
            streaks — applied to AI fluency. The first lesson is always the same: say hello, then say why
            you're here. Try it below.
          </p>
          <p className="mt-4 text-[15px] text-ink-soft">
            This is a live preview of Lesson 1 — go ahead, type something real.
          </p>
        </div>

        <div className="mx-auto w-full max-w-md rounded-2xl border border-border bg-surface p-6 shadow-lift" data-testid="card-microlesson-demo">
          <div className="flex items-center justify-between border-b border-border pb-4">
            <div className="text-sm font-semibold text-ink">Lesson 1 · Say hello to AI</div>
            <div className="flex items-center gap-3 text-sm font-semibold">
              <span className="flex items-center gap-1 text-ember-600">
                <Flame className="h-4 w-4" />1
              </span>
              <span className="flex items-center gap-1 text-iris-600">
                <Sparkles className="h-4 w-4" />
                {xp} XP
              </span>
            </div>
          </div>

          <div className="min-h-[15rem] py-5">
            {step === "intro" && (
              <div className="flex h-full flex-col items-start gap-4">
                <p className="text-[15px] text-ink-muted">
                  Every journey starts the same way for everyone: high schooler, business owner, doesn't matter.
                  You send one message, then you tell it who you are.
                </p>
                <Button onClick={() => setStep("hello")} data-testid="button-start-lesson">
                  Start the lesson
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            )}

            {step === "hello" && (
              <form onSubmit={submitHello} className="flex h-full flex-col gap-4">
                <div className="max-w-[90%] rounded-2xl rounded-tl-sm bg-iris-50 px-4 py-3 text-sm text-ink">
                  Type <span className="font-semibold">"Hello"</span> — or anything — to send your first prompt.
                </div>
                <Input
                  autoFocus
                  value={helloText}
                  onChange={(e) => setHelloText(e.target.value)}
                  placeholder="Hello"
                  data-testid="input-lesson-hello"
                />
                <Button type="submit" disabled={!helloText.trim()} data-testid="button-submit-hello">
                  Send
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </form>
            )}

            {step === "why" && (
              <form onSubmit={submitWhy} className="flex h-full flex-col gap-4">
                <div className="max-w-[90%] rounded-2xl rounded-tl-sm bg-iris-50 px-4 py-3 text-sm text-ink">
                  Nice — that's a real prompt. Now finish this: "My name is ___ and I want AI to help me ___."
                </div>
                <Input
                  autoFocus
                  value={whyText}
                  onChange={(e) => setWhyText(e.target.value)}
                  placeholder="My name is Alex and I want AI to help me..."
                  data-testid="input-lesson-why"
                />
                <Button type="submit" disabled={!whyText.trim()} data-testid="button-submit-why">
                  Send
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </form>
            )}

            {step === "done" && (
              <div className="flex h-full flex-col gap-4">
                <div className="max-w-[95%] rounded-2xl rounded-tl-sm bg-iris-50 px-4 py-3 text-sm text-ink">
                  That's it. That's the whole framework — "{whyText}" is your why, and it's the seed of your
                  entire AI copilot.
                </div>
                <div className="flex items-center justify-between rounded-xl bg-moss-100 px-4 py-3 text-sm font-semibold text-moss-600">
                  <span>Lesson complete</span>
                  <span>+{XP_PER_STEP.hello + XP_PER_STEP.why} XP</span>
                </div>
                <div className="mt-1 flex flex-col gap-2 sm:flex-row">
                  <Button asChild data-testid="button-save-streak">
                    <a href="#waitlist">Save my streak</a>
                  </Button>
                  <Button variant="ghost" onClick={reset} data-testid="button-replay-lesson">
                    <RotateCcw className="h-4 w-4" />
                    Replay
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
