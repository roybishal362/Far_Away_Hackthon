"use client";

import { useEffect, useState } from "react";
import { Lock, Database, EyeOff, FileCheck2 } from "lucide-react";
import { streamRun, loadPlan } from "@/lib/api";
import { Profile, RunResult, StepEvent } from "@/lib/types";
import { Hero } from "@/components/Hero";
import { IntakeForm } from "@/components/IntakeForm";
import { AgentTimeline } from "@/components/AgentTimeline";
import { ResultsPanel } from "@/components/Results";

const PRIVACY = [
  { icon: <Database className="h-4 w-4" />, t: "Data minimization", d: "Only the fields you enter; no account, no tracking." },
  { icon: <Lock className="h-4 w-4" />, t: "Encrypted at rest", d: "Any stored profile uses AES (Fernet)." },
  { icon: <EyeOff className="h-4 w-4" />, t: "No PII in logs", d: "Profiles are redacted to coarse signals before logging." },
  { icon: <FileCheck2 className="h-4 w-4" />, t: "Official sources", d: "Every claim links to ssw.go.jp / MOFA." },
];

export default function Page() {
  const [steps, setSteps] = useState<StepEvent[]>([]);
  const [result, setResult] = useState<RunResult | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);

  // Load a shared plan if the URL has ?plan=<id>
  useEffect(() => {
    const id = new URLSearchParams(window.location.search).get("plan");
    if (id) loadPlan(id).then(setResult).catch(() => {});
  }, []);

  async function handleRun(p: Profile) {
    setProfile(p);
    setSteps([]);
    setResult(null);
    setError(null);
    setRunning(true);
    try {
      await streamRun(p, {
        onStep: (s) => setSteps((prev) => [...prev, s]),
        onResult: (r) => setResult(r),
        onError: (e) => setError(e.message),
      });
    } catch (e: any) {
      setError(e.message ?? "Connection failed — is the API running on :8000?");
    } finally {
      setRunning(false);
    }
  }

  return (
    <main className="min-h-screen pb-24">
      <Hero />

      <section id="start" className="container-app mt-6 scroll-mt-8">
        <div className="grid items-start gap-6 lg:grid-cols-2">
          <IntakeForm onRun={handleRun} loading={running} />
          <AgentTimeline steps={steps} running={running} />
        </div>

        {error && (
          <div className="card mt-6 border-red-200 bg-red-50 text-sm text-red-700">⚠️ {error}</div>
        )}

        {result && (
          <div className="mt-10">
            <ResultsPanel result={result} profile={profile} />
          </div>
        )}
      </section>

      {/* Privacy / trust */}
      <section className="container-app mt-16">
        <div className="card">
          <h3 className="font-display text-2xl">Private &amp; trustworthy by design</h3>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {PRIVACY.map((p) => (
              <div key={p.t} className="rounded-xl bg-black/[0.02] p-4">
                <div className="flex items-center gap-2 text-ink">{p.icon}<span className="font-medium">{p.t}</span></div>
                <p className="mt-1 text-xs text-ink/55">{p.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="container-app mt-16 text-center text-sm text-ink/40">
        <p className="font-display text-lg text-bridge">Kakehashi 架け橋</p>
        <p className="mt-1">A bridge between India and Japan · FAR AWAY 2026 · Agentic &amp; Autonomous Systems</p>
        <p className="mx-auto mt-4 max-w-2xl text-xs text-ink/35">
          ⚠️ Guidance grounded in official sources — not legal or immigration advice. Always verify current rules,
          fees, and dates with the official authorities (ISA, MOFA, Japan Foundation, Prometric). Information current as of June 2026.
        </p>
      </footer>
    </main>
  );
}
