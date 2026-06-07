import Link from "next/link";
import {
  ArrowRight, ShieldCheck, Globe, FileText, Briefcase, GraduationCap,
  MessageCircle, MapPin, Database, Lock, EyeOff, FlaskConical,
} from "lucide-react";
import { Hero } from "@/components/Hero";

const STEPS = [
  { n: 1, t: "Tell us about you", d: "Skills, experience, Japanese level — or just upload your resume. Choose EN / हिन्दी / 日本語." },
  { n: 2, t: "Agents go to work", d: "Specialized AI agents read official Japanese sources and live job data, citing every claim — you watch them think live." },
  { n: 3, t: "Get a real, proven plan", d: "Eligibility, real jobs ranked to you, step-by-step with official links, a study plan, and costs — save, share, or download as PDF." },
];

const FEATURES = [
  { icon: <MapPin className="h-5 w-5" />, t: "Personalized pathway", d: "A verdict, readiness score and gap analysis built from your actual profile — IT/office roles auto-routed to the right visa." },
  { icon: <Briefcase className="h-5 w-5" />, t: "Real live jobs", d: "Actual openings in Japan, ranked by fit to you with a reason — not mock data." },
  { icon: <FileText className="h-5 w-5" />, t: "Step-by-step with real links", d: "Every step links to the official site (ISA, JFT-Basic, Prometric, JLPT…) and what it's for." },
  { icon: <GraduationCap className="h-5 w-5" />, t: "Study plan + free resources", d: "A plan keyed to your Japanese level, with free open-source materials (Irodori, JLPT, NHK Easy…)." },
  { icon: <FlaskConical className="h-5 w-5" />, t: "Proof, not claims", d: "A built-in ablation measures grounded vs. ungrounded accuracy and hallucinations." },
  { icon: <MessageCircle className="h-5 w-5" />, t: "Ask anything", d: "A grounded chat answers your follow-ups with citations — in your language." },
];

const TRUST = [
  { icon: <Database className="h-4 w-4" />, t: "Real or nothing", d: "Every fact is from a real API or a cited official document — never fabricated." },
  { icon: <Lock className="h-4 w-4" />, t: "Encrypted at rest", d: "Any saved profile uses AES (Fernet)." },
  { icon: <EyeOff className="h-4 w-4" />, t: "No PII in logs", d: "Profiles are redacted to coarse signals before logging." },
  { icon: <Globe className="h-4 w-4" />, t: "EN / हिन्दी / 日本語", d: "Content and chat in your language." },
];

function Section({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={"container-app mt-20 " + className}>{children}</section>;
}

export default function Landing() {
  return (
    <main>
      <Hero />

      {/* How it works */}
      <Section>
        <h2 className="font-display text-3xl">How it works</h2>
        <p className="mt-1 text-ink/60">From "where do I start?" to a real, proven plan — in one run.</p>
        <div className="mt-6 grid gap-5 md:grid-cols-3">
          {STEPS.map((s) => (
            <div key={s.n} className="card">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-r from-sakura-600 to-marigold-500 font-display text-lg text-white">{s.n}</div>
              <h3 className="mt-3 font-display text-xl">{s.t}</h3>
              <p className="mt-1 text-sm text-ink/65">{s.d}</p>
            </div>
          ))}
        </div>
      </Section>

      {/* Impact */}
      <Section>
        <div className="card bg-gradient-to-br from-indigo-800 to-sakura-600 text-white">
          <h2 className="font-display text-3xl">Why this matters</h2>
          <p className="mt-2 max-w-3xl text-white/85">
            In August 2025, India and Japan signed a pact to move <b>50,000 skilled Indian workers</b> to Japan, which
            faces a deep labour shortage. But the journey — visa, the JLPT N4 language bar, skills tests, paperwork,
            job matching — is a confusing, months-long maze. Kakehashi is the autonomous guide through it, serving
            <b> both governments</b>: India sends workers, Japan fills its gap.
          </p>
          <div className="mt-6 grid grid-cols-3 gap-4">
            {[["50,000", "Indian workers → Japan (2025 pact)"], ["19", "eligible SSW sectors"], ["0", "hallucinations (grounded)"]].map(([v, l]) => (
              <div key={l} className="rounded-xl bg-white/10 p-4">
                <div className="font-display text-3xl">{v}</div>
                <div className="mt-1 text-xs text-white/75">{l}</div>
              </div>
            ))}
          </div>
        </div>
      </Section>

      {/* Features */}
      <Section>
        <h2 className="font-display text-3xl">Everything in one place</h2>
        <div className="mt-6 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div key={f.t} className="card">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sakura-50 text-sakura-600">{f.icon}</div>
              <h3 className="mt-3 font-display text-lg">{f.t}</h3>
              <p className="mt-1 text-sm text-ink/65">{f.d}</p>
            </div>
          ))}
        </div>
      </Section>

      {/* Trust */}
      <Section>
        <div className="card">
          <h2 className="flex items-center gap-2 font-display text-2xl"><ShieldCheck className="h-6 w-6 text-emerald-600" /> Private &amp; trustworthy by design</h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {TRUST.map((p) => (
              <div key={p.t} className="rounded-xl bg-black/[0.02] p-4">
                <div className="flex items-center gap-2 text-ink">{p.icon}<span className="font-medium">{p.t}</span></div>
                <p className="mt-1 text-xs text-ink/55">{p.d}</p>
              </div>
            ))}
          </div>
        </div>
      </Section>

      {/* CTA */}
      <Section>
        <div className="card flex flex-col items-center gap-4 py-12 text-center">
          <h2 className="font-display text-3xl">Ready to find your path to Japan?</h2>
          <p className="max-w-xl text-ink/65">Free, grounded in official sources, and personalized to you in minutes.</p>
          <Link href="/app" className="btn-primary text-base">Build my migration plan <ArrowRight className="h-4 w-4" /></Link>
        </div>
      </Section>
    </main>
  );
}
