import { useEffect, useState, type FormEvent } from "react";
import { CheckCircle2, Loader2, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

const personaOptions = [
  { value: "high-schooler", label: "High schooler" },
  { value: "career-changer", label: "Career changer / mid-career professional" },
  { value: "later-in-life", label: "Later-in-life learner" },
  { value: "small-business", label: "Small or medium business owner" },
  { value: "curious", label: "Just curious" },
];

type Status = "idle" | "submitting" | "success" | "error";

export default function WaitlistSection() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [persona, setPersona] = useState("");
  const [why, setWhy] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [message, setMessage] = useState("");
  const [count, setCount] = useState<number | null>(null);

  useEffect(() => {
    fetch("/api/waitlist/count")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && typeof data.count === "number") setCount(data.count);
      })
      .catch(() => {});
  }, [status]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setStatus("submitting");
    setMessage("");

    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, persona, why }),
      });
      const data = await res.json();

      if (!res.ok) {
        setStatus("error");
        setMessage(data.message ?? "Something went wrong. Please try again.");
        return;
      }

      setStatus("success");
      setMessage(`You're in, ${data.name?.split(" ")[0] ?? "friend"}. We'll email you when your first lesson is ready.`);
    } catch {
      setStatus("error");
      setMessage("Couldn't reach the server. Please try again in a moment.");
    }
  }

  if (status === "success") {
    return (
      <section id="waitlist" className="border-t border-border py-20">
        <div className="container-page">
          <div className="mx-auto max-w-lg rounded-2xl border border-moss-100 bg-moss-100/40 p-8 text-center">
            <CheckCircle2 className="mx-auto h-10 w-10 text-moss-600" />
            <h2 className="mt-4 text-2xl font-bold text-ink">You're on the list</h2>
            <p className="mt-2 text-[15px] text-ink-muted">{message}</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="waitlist" className="border-t border-border py-20">
      <div className="container-page grid gap-12 lg:grid-cols-[1fr_1.1fr] lg:items-start">
        <div>
          <span className="text-sm font-semibold uppercase tracking-wide text-iris-600">Get started</span>
          <h2 className="mt-3 text-balance text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Your first small win is two minutes away.
          </h2>
          <p className="mt-4 text-lg text-ink-muted">
            Tell us a little about you and we'll send your first lesson — built from your why, not a
            generic curriculum.
          </p>
          {count !== null && (
            <p className="mt-6 flex items-center gap-2 text-sm font-medium text-ink-muted" data-testid="text-waitlist-count">
              <Users className="h-4 w-4 text-iris-500" />
              {count === 0 ? "Be the first to join" : `${count} ${count === 1 ? "person has" : "people have"} already joined`}
            </p>
          )}
        </div>

        <form onSubmit={handleSubmit} className="rounded-2xl border border-border bg-surface p-6 shadow-soft sm:p-8">
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <Label htmlFor="name">Your name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Jordan Rivera" required data-testid="input-waitlist-name" />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required data-testid="input-waitlist-email" />
            </div>
          </div>

          <div className="mt-5">
            <Label htmlFor="persona">Which best describes you?</Label>
            <select
              id="persona"
              value={persona}
              onChange={(e) => setPersona(e.target.value)}
              required
              data-testid="select-waitlist-persona"
              className="flex h-11 w-full rounded-xl border border-border bg-surface px-4 text-[15px] text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-iris-500"
            >
              <option value="" disabled>
                Choose one
              </option>
              {personaOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div className="mt-5">
            <Label htmlFor="why">What's your why? (optional)</Label>
            <Textarea id="why" value={why} onChange={(e) => setWhy(e.target.value)} placeholder="I want AI to help me..." data-testid="input-waitlist-why" />
          </div>

          {status === "error" && (
            <p className="mt-4 text-sm font-medium text-ember-700" role="alert" data-testid="text-waitlist-error">
              {message}
            </p>
          )}

          <Button type="submit" size="lg" className="mt-6 w-full" disabled={status === "submitting"} data-testid="button-waitlist-submit">
            {status === "submitting" ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Joining...
              </>
            ) : (
              "Save my spot"
            )}
          </Button>
        </form>
      </div>
    </section>
  );
}
