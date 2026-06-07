import Link from "next/link";
import { ArrowRight, ShieldCheck, FlaskConical, Boxes, Database, Languages } from "lucide-react";

export const metadata = {
  title: "How Kakehashi works — agentic architecture & proof",
  description: "The agentic multi-agent system, source-grounding, and the proof behind Kakehashi.",
};

const AGENTS = [
  { e: "🧭", n: "Pathway", d: "Classifies the correct visa (SSW / Engineer / Specialist) and gives a personalized eligibility verdict + readiness score, grounded in official rules." },
  { e: "💼", n: "Jobs", d: "Fetches real live openings in Japan and ranks each by fit to your profile, with a reason." },
  { e: "📄", n: "Procedure", d: "Serves the official ordered journey — each step links to the real government site and explains its purpose." },
  { e: "📚", n: "Prep", d: "Builds a study + exam plan keyed to your Japanese level, with free open-source resources." },
  { e: "🗓️", n: "Journey", d: "Relocation, flight & timeline planning (Round 2 — Amadeus wired)." },
  { e: "✨", n: "Synthesis", d: "Composes your warm personal overview plus concrete salary and cost figures." },
];

const STACK = [
  { icon: <Boxes className="h-5 w-5" />, t: "Agentic backend", d: "FastAPI orchestrates specialized agents over a UI-agnostic core; the live timeline streams via SSE. Adaptive — it skips steps that don't apply to your route." },
  { icon: <Database className="h-5 w-5" />, t: "Real data only", d: "Official SSW facts (RAG + BM25, every claim cited), live jobs API, and Japan government statistics. Tools physically cannot fabricate — no key, no data." },
  { icon: <FlaskConical className="h-5 w-5" />, t: "Measured proof", d: "A built-in ablation runs the same question grounded vs. ungrounded and scores both against a gold set — turning 'trust us' into a number." },
  { icon: <Languages className="h-5 w-5" />, t: "Multilingual", d: "Content and chat in English, Hindi and Japanese, powered by a strong multilingual model." },
];

function Section({ children }: { children: React.ReactNode }) {
  return <section className="container-app mt-16">{children}</section>;
}

export default function How() {
  return (
    <main className="pt-12">
      <div className="container-app">
        <span className="chip">Agentic &amp; Autonomous Systems</span>
        <h1 className="mt-4 font-display text-4xl sm:text-5xl">How Kakehashi works</h1>
        <p className="mt-3 max-w-2xl text-lg text-ink/70">
          A team of autonomous agents that perceive your situation, reason over official sources, act with real tools,
          and prove their answers — then keep helping you via chat.
        </p>
      </div>

      <Section>
        <h2 className="font-display text-3xl">The multi-agent system</h2>
        <p className="mt-1 text-ink/60">Each agent reasons with an LLM, calls a real tool, and cites its sources.</p>
        <div className="mt-6 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {AGENTS.map((a) => (
            <div key={a.n} className="card">
              <div className="text-2xl">{a.e}</div>
              <h3 className="mt-2 font-display text-xl">{a.n}</h3>
              <p className="mt-1 text-sm text-ink/65">{a.d}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section>
        <h2 className="font-display text-3xl">What makes it trustworthy</h2>
        <div className="mt-6 grid gap-5 md:grid-cols-2">
          {STACK.map((s) => (
            <div key={s.t} className="card">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-800/10 text-indigo-800">{s.icon}</div>
              <h3 className="mt-3 font-display text-lg">{s.t}</h3>
              <p className="mt-1 text-sm text-ink/65">{s.d}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section>
        <div className="card flex flex-col items-center gap-4 py-12 text-center">
          <ShieldCheck className="h-10 w-10 text-emerald-600" />
          <h2 className="font-display text-3xl">See it for yourself</h2>
          <p className="max-w-xl text-ink/65">Run it, then open the Proof tab to see grounded-vs-ungrounded accuracy and hallucinations measured live.</p>
          <Link href="/app" className="btn-primary text-base">Try it now <ArrowRight className="h-4 w-4" /></Link>
        </div>
      </Section>
    </main>
  );
}
