import Link from "next/link";
import {
  ArrowRight, FlaskConical, Boxes, Database, Languages,
  Brain, Wrench, Quote, BadgeCheck,
} from "lucide-react";
import { Reveal } from "@/components/Reveal";

export const metadata = {
  title: "How Kakehashi works — agentic architecture & proof",
  description: "The agentic multi-agent system, source-grounding, and the proof behind Kakehashi.",
};

const REPO = "https://github.com/roybishal362/Kakehashi";

const LOOP = [
  { icon: <Brain className="h-5 w-5" />, t: "Reason", d: "The agent thinks about your specific situation with an LLM — what applies to you, and what to check." },
  { icon: <Wrench className="h-5 w-5" />, t: "Call a real tool", d: "It hits a real source — official SSW facts, the live jobs API, or government data. No key, no data — it won't invent one." },
  { icon: <Quote className="h-5 w-5" />, t: "Cite the source", d: "Every claim carries the official URL it came from, so you (and judges) can verify it." },
  { icon: <BadgeCheck className="h-5 w-5" />, t: "Score confidence", d: "It rates how sure it is. Low confidence or missing data is shown honestly, never hidden." },
];

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
  { icon: <FlaskConical className="h-5 w-5" />, t: "Measured proof", d: "A built-in test runs the same question grounded vs. ungrounded and scores both against a gold set — turning 'trust us' into a number." },
  { icon: <Languages className="h-5 w-5" />, t: "Multilingual", d: "Content and chat in English, Hindi and Japanese, powered by a strong multilingual model." },
];

export default function How() {
  return (
    <main>
      {/* Hero band */}
      <header className="relative isolate overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/fuji-sakura.jpg" alt="Mount Fuji and spring blossoms" className="absolute inset-0 -z-20 h-full w-full object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-white via-white/90 to-white/20 sm:to-white/5" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-t from-[#fbf9fb] via-transparent to-transparent" />
        <div className="container-app pb-16 pt-16 sm:pt-20">
          <Reveal className="max-w-2xl">
            <span className="chip shadow-sm">Agentic &amp; Autonomous Systems</span>
            <h1 className="mt-4 font-display text-4xl font-extrabold leading-[1.05] sm:text-6xl">How Kakehashi works</h1>
            <p className="mt-4 max-w-xl text-lg text-ink/75">
              A team of autonomous agents that read your situation, reason over official sources, act with real tools,
              and prove their answers — then keep helping you in chat.
            </p>
            <Link href="/app" className="btn-primary mt-6">
              Try it now <ArrowRight className="h-4 w-4" />
            </Link>
          </Reveal>
        </div>
      </header>

      {/* The honest loop */}
      <section className="container-app mt-20">
        <Reveal>
          <span className="eyebrow">The pattern</span>
          <h2 className="mt-2 font-display text-3xl font-bold sm:text-4xl">Every agent follows the same honest loop.</h2>
        </Reveal>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {LOOP.map((s, i) => (
            <Reveal key={s.t} delay={i * 0.08} className="card relative">
              <div className="absolute right-5 top-4 font-display text-4xl font-extrabold text-black/[0.05]">{i + 1}</div>
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-sakura-50 text-sakura-600">{s.icon}</div>
              <h3 className="mt-4 font-display text-lg font-semibold">{s.t}</h3>
              <p className="mt-1 text-sm text-ink/65">{s.d}</p>
            </Reveal>
          ))}
        </div>
      </section>

      {/* The six agents */}
      <section className="container-app mt-24">
        <Reveal>
          <span className="eyebrow">The team</span>
          <h2 className="mt-2 font-display text-3xl font-bold sm:text-4xl">Six specialized agents</h2>
          <p className="mt-2 max-w-2xl text-ink/60">
            Each reasons with an LLM, calls a real tool, and cites its sources. The orchestrator runs only the ones
            your route actually needs.
          </p>
        </Reveal>
        <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {AGENTS.map((a, i) => (
            <Reveal key={a.n} delay={(i % 3) * 0.07} className="group card transition hover:-translate-y-1 hover:shadow-glow">
              <div className="text-3xl">{a.e}</div>
              <h3 className="mt-3 font-display text-xl font-semibold">{a.n}</h3>
              <p className="mt-1 text-sm text-ink/65">{a.d}</p>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Why trust it — immersive dark band */}
      <section className="relative isolate mt-24 overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/tokyo.jpg" alt="Tokyo at dusk" className="absolute inset-0 -z-20 h-full w-full object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-900/96 via-indigo-900/92 to-sakura-600/70" />
        <div className="container-app py-20 sm:py-24 text-white">
          <Reveal>
            <span className="eyebrow text-sakura-300">Why trust it</span>
            <h2 className="mt-2 font-display text-3xl font-bold sm:text-4xl">Built so it can&apos;t bluff.</h2>
          </Reveal>
          <div className="mt-10 grid gap-5 md:grid-cols-2">
            {STACK.map((s, i) => (
              <Reveal key={s.t} delay={i * 0.08} className="glass p-6 text-white">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white/15 text-white">{s.icon}</div>
                <h3 className="mt-3 font-display text-lg font-semibold">{s.t}</h3>
                <p className="mt-1 text-sm text-white/75">{s.d}</p>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Proof callout */}
      <section className="container-app mt-24">
        <Reveal className="card flex flex-col items-center gap-4 py-12 text-center">
          <FlaskConical className="h-10 w-10 text-sakura-600" />
          <h2 className="font-display text-3xl font-bold">We turned &ldquo;trust us&rdquo; into a number.</h2>
          <p className="max-w-xl text-ink/65">
            Run it, then open the <b>Proof</b> tab to see grounded-vs-ungrounded accuracy and made-up facts measured
            live — <b className="text-ink">51% vs 4%</b> accuracy, and <b className="text-ink">0 vs 69</b> contradictions
            of official facts.
          </p>
          <div className="mt-2 flex flex-wrap justify-center gap-3">
            <Link href="/app" className="btn-primary">Try it now <ArrowRight className="h-4 w-4" /></Link>
            <a href={`${REPO}/blob/main/PROOF.md`} target="_blank" rel="noreferrer" className="btn-ghost">Read the proof</a>
          </div>
        </Reveal>
      </section>

      {/* Final CTA — Fuji sunrise */}
      <section className="relative isolate mt-24 overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/hero-fuji.png" alt="Mount Fuji and a bridge at sunrise" className="absolute inset-0 -z-20 h-full w-full object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-white via-white/88 to-white/30" />
        <div className="container-app py-20 sm:py-24">
          <Reveal className="max-w-xl">
            <h2 className="font-display text-3xl font-bold leading-tight sm:text-5xl">See it for yourself.</h2>
            <p className="mt-4 text-lg text-ink/70">One run shows you the whole journey — cited, personalized, and proven.</p>
            <Link href="/app" className="btn-primary mt-7 text-base">Build my migration plan <ArrowRight className="h-4 w-4" /></Link>
          </Reveal>
        </div>
      </section>

      <div className="h-20" />
    </main>
  );
}
