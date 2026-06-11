import {
  ArrowRight, ShieldCheck, Globe, FileText, Briefcase, GraduationCap,
  MessageCircle, MapPin, Database, Lock, EyeOff, FlaskConical,
} from "lucide-react";
import { Hero } from "@/components/Hero";
import { Reveal } from "@/components/Reveal";

const REPO = "https://github.com/roybishal362/Kakehashi";

const SOURCES = ["出入国在留管理庁 ISA", "外務省 MOFA", "厚生労働省 MHLW", "JFT-Basic", "JLPT", "PIB India"];

const BIG_STATS: [string, string, string][] = [
  ["500,000", "people exchanged both ways over five years", "Aug-2025 Action Plan"],
  ["50,000", "skilled Indian workers heading to Japan", "India → Japan"],
  ["~570,000", "care-worker shortfall Japan faces by 2040", "MHLW"],
];

const STEPS = [
  { n: 1, t: "Tell us about you", d: "Skills, experience, Japanese level — or just upload your resume. Choose EN / हिन्दी / 日本語." },
  { n: 2, t: "Agents go to work", d: "Specialized AI agents read official Japanese sources and live job data, citing every claim — you watch them think, live." },
  { n: 3, t: "Get a real, proven plan", d: "Eligibility, real jobs ranked to you, official steps with links, a study plan, and costs — save, share, or download as a PDF." },
];

const FEATURES = [
  { icon: <MapPin className="h-5 w-5" />, t: "Personalized pathway", d: "A verdict, readiness score and gap analysis from your actual profile — IT/office roles auto-routed to the right visa." },
  { icon: <Briefcase className="h-5 w-5" />, t: "Real live jobs", d: "Actual openings in Japan, ranked by fit to you with a reason — not mock data." },
  { icon: <FileText className="h-5 w-5" />, t: "Steps with real links", d: "Every step links to the official site (ISA, JFT-Basic, Prometric, JLPT…) and explains what it's for." },
  { icon: <GraduationCap className="h-5 w-5" />, t: "Study plan + free resources", d: "A plan keyed to your Japanese level, with free open materials (Irodori, JLPT, NHK Easy…)." },
  { icon: <FlaskConical className="h-5 w-5" />, t: "Proof, not claims", d: "A built-in test measures grounded vs. ungrounded accuracy and made-up facts." },
  { icon: <MessageCircle className="h-5 w-5" />, t: "Ask anything", d: "A grounded chat answers your follow-ups with citations — in your language." },
];

const TRUST = [
  { icon: <Database className="h-4 w-4" />, t: "Real or nothing", d: "Every fact is from a real API or a cited official document — never fabricated." },
  { icon: <Lock className="h-4 w-4" />, t: "Encrypted at rest", d: "Any saved profile uses AES (Fernet)." },
  { icon: <EyeOff className="h-4 w-4" />, t: "No PII in logs", d: "Profiles are redacted to coarse signals before logging." },
  { icon: <Globe className="h-4 w-4" />, t: "EN / हिन्दी / 日本語", d: "Content and chat in your language." },
];

export default function Landing() {
  return (
    <main>
      <Hero />

      {/* Source trust strip */}
      <section className="container-app mt-16">
        <p className="text-center text-xs font-semibold uppercase tracking-[0.2em] text-ink/40">
          Grounded in official sources
        </p>
        <div className="mt-4 flex flex-wrap items-center justify-center gap-x-8 gap-y-3 text-sm font-medium text-ink/45">
          {SOURCES.map((s) => (
            <span key={s}>{s}</span>
          ))}
        </div>
      </section>

      {/* Why this matters — immersive dark band (Tokyo at dusk) */}
      <section className="relative isolate mt-20 overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/tokyo.jpg" alt="Tokyo skyline at dusk" className="absolute inset-0 -z-20 h-full w-full object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-900/96 via-indigo-900/90 to-sakura-600/75" />
        <div className="container-app py-20 sm:py-24">
          <Reveal className="max-w-3xl text-white">
            <span className="eyebrow text-sakura-300">The opportunity</span>
            <h2 className="mt-3 font-display text-3xl font-bold leading-tight sm:text-5xl">
              Two governments opened the door.<br className="hidden sm:block" /> The worker still has to find it.
            </h2>
            <p className="mt-5 max-w-2xl text-lg text-white/80">
              In <b className="text-white">August 2025</b>, India and Japan signed a pact to move 50,000 skilled
              Indians to Japan over five years. But for one real person, the path is a months-long maze — the visa,
              the JLPT&nbsp;N4 language bar, skills tests, paperwork, and finding an honest employer. Kakehashi is the
              autonomous guide through it.
            </p>
          </Reveal>
          <div className="mt-12 grid gap-4 sm:grid-cols-3">
            {BIG_STATS.map(([v, l, src], i) => (
              <Reveal key={l} delay={i * 0.1} className="glass p-6 text-white">
                <div className="font-display text-4xl font-extrabold sm:text-5xl">{v}</div>
                <div className="mt-2 text-sm text-white/80">{l}</div>
                <div className="mt-3 text-[11px] uppercase tracking-wide text-white/45">{src}</div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="container-app mt-24">
        <Reveal>
          <span className="eyebrow">How it works</span>
          <h2 className="mt-2 font-display text-3xl font-bold sm:text-4xl">
            From &ldquo;where do I start?&rdquo; to a real plan — in one run.
          </h2>
        </Reveal>
        <div className="mt-8 grid gap-5 md:grid-cols-3">
          {STEPS.map((s, i) => (
            <Reveal key={s.n} delay={i * 0.08} className="card">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-sakura-600 to-marigold-500 font-display text-lg font-bold text-white shadow-glow">
                {s.n}
              </div>
              <h3 className="mt-4 font-display text-xl font-semibold">{s.t}</h3>
              <p className="mt-2 text-sm text-ink/65">{s.d}</p>
            </Reveal>
          ))}
        </div>
      </section>

      {/* The proof */}
      <section className="container-app mt-24">
        <Reveal className="overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-900 to-indigo-800 p-7 text-white shadow-card sm:p-10">
          <div className="grid items-center gap-8 lg:grid-cols-2">
            <div>
              <span className="eyebrow text-sakura-300">The proof</span>
              <h2 className="mt-2 font-display text-3xl font-bold sm:text-4xl">
                We don&apos;t claim it&apos;s accurate. We measure it.
              </h2>
              <p className="mt-4 text-white/75">
                The same questions, asked two ways, scored by a judge against <b className="text-white">22 official
                SSW facts</b>. Grounding makes the answers far more accurate — and removes every made-up
                &ldquo;fact.&rdquo; Fully reproducible, with the raw verdicts committed to the repo.
              </p>
              <a href={`${REPO}/blob/main/PROOF.md`} target="_blank" rel="noreferrer" className="btn-light mt-6">
                See the proof <ArrowRight className="h-4 w-4" />
              </a>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="glass p-5">
                <div className="text-xs font-semibold uppercase tracking-wide text-emerald-300">✅ Grounded (us)</div>
                <div className="mt-3 font-display text-4xl font-extrabold">51%</div>
                <div className="text-sm text-white/65">accuracy</div>
                <div className="mt-4 font-display text-4xl font-extrabold">0</div>
                <div className="text-sm text-white/65">made-up facts</div>
              </div>
              <div className="glass p-5">
                <div className="text-xs font-semibold uppercase tracking-wide text-white/50">❌ Plain LLM</div>
                <div className="mt-3 font-display text-4xl font-extrabold text-white/55">4%</div>
                <div className="text-sm text-white/45">accuracy</div>
                <div className="mt-4 font-display text-4xl font-extrabold text-sakura-300">69</div>
                <div className="text-sm text-white/45">made-up facts</div>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

      {/* Features */}
      <section className="container-app mt-24">
        <Reveal>
          <span className="eyebrow">Everything in one place</span>
          <h2 className="mt-2 font-display text-3xl font-bold sm:text-4xl">One run. Your whole journey, mapped.</h2>
        </Reveal>
        <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f, i) => (
            <Reveal key={f.t} delay={(i % 3) * 0.07} className="group card transition hover:-translate-y-1 hover:shadow-glow">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-sakura-50 text-sakura-600 transition group-hover:bg-sakura-600 group-hover:text-white">
                {f.icon}
              </div>
              <h3 className="mt-4 font-display text-lg font-semibold">{f.t}</h3>
              <p className="mt-2 text-sm text-ink/65">{f.d}</p>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Emotional band — lantern-lit street */}
      <section className="relative isolate mt-24 overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/lanterns.jpg" alt="A lantern-lit street in Japan at night" className="absolute inset-0 -z-20 h-full w-full object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-t from-indigo-900/95 via-indigo-900/80 to-indigo-900/55" />
        <div className="container-app py-24 text-center">
          <Reveal className="mx-auto max-w-2xl text-white">
            <h2 className="font-display text-3xl font-bold leading-tight sm:text-5xl">
              A real life in Japan — built on honest ground.
            </h2>
            <p className="mt-5 text-lg text-white/80">
              No fake agents. No hidden fees. Just official facts, your real options, and a plan you own —
              downloadable as a PDF, in your language.
            </p>
            <a href="/app" className="btn-primary mt-8 text-base">
              Start my plan — free <ArrowRight className="h-4 w-4" />
            </a>
          </Reveal>
        </div>
      </section>

      {/* Trust */}
      <section className="container-app mt-24">
        <div className="card">
          <h2 className="flex items-center gap-2 font-display text-2xl font-semibold">
            <ShieldCheck className="h-6 w-6 text-emerald-600" /> Private &amp; trustworthy by design
          </h2>
          <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {TRUST.map((p) => (
              <div key={p.t} className="rounded-xl bg-black/[0.02] p-4">
                <div className="flex items-center gap-2 text-ink">
                  {p.icon}
                  <span className="font-medium">{p.t}</span>
                </div>
                <p className="mt-1 text-xs text-ink/55">{p.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA — Fuji at sunrise */}
      <section className="relative isolate mt-24 overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/hero-fuji.png" alt="Mount Fuji and a bridge at sunrise" className="absolute inset-0 -z-20 h-full w-full object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-white via-white/88 to-white/30" />
        <div className="container-app py-20 sm:py-24">
          <Reveal className="max-w-xl">
            <h2 className="font-display text-3xl font-bold leading-tight sm:text-5xl">Ready to find your path to Japan?</h2>
            <p className="mt-4 text-lg text-ink/70">Free, grounded in official sources, and personalized to you in minutes.</p>
            <a href="/app" className="btn-primary mt-7 text-base">
              Build my migration plan <ArrowRight className="h-4 w-4" />
            </a>
          </Reveal>
        </div>
      </section>

      <div className="h-20" />
    </main>
  );
}
