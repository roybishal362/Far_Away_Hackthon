"use client";

import { useEffect, useRef, useState } from "react";
import { streamRun, loadPlan } from "@/lib/api";
import { Profile, RunResult, StepEvent } from "@/lib/types";
import { IntakeForm } from "@/components/IntakeForm";
import { AgentTimeline } from "@/components/AgentTimeline";
import { ResultsPanel } from "@/components/Results";

export default function AppPage() {
  const [steps, setSteps] = useState<StepEvent[]>([]);
  const [result, setResult] = useState<RunResult | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  // Load a shared plan if the URL has ?plan=<id>
  useEffect(() => {
    const id = new URLSearchParams(window.location.search).get("plan");
    if (id) {
      loadPlan(id)
        .then(({ result, profile }) => { setResult(result); setProfile(profile); })
        .catch(() => setError("This shared plan has expired or wasn't found. Build a fresh one below."));
    }
  }, []);

  async function handleRun(p: Profile) {
    // Cancel any in-flight run so rapid clicks / language switches don't interleave.
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setProfile(p);
    setSteps([]);
    setResult(null);
    setError(null);
    setRunning(true);
    try {
      await streamRun(p, {
        onStep: (s) => { if (!controller.signal.aborted) setSteps((prev) => [...prev, s]); },
        onResult: (r) => { if (!controller.signal.aborted) setResult(r); },
        onError: (e) => { if (!controller.signal.aborted) setError(e.message); },
      }, controller.signal);
    } catch (e: any) {
      if (e?.name !== "AbortError" && !controller.signal.aborted) {
        setError(e?.message ?? "Connection failed — is the API running on :8000?");
      }
    } finally {
      if (abortRef.current === controller) setRunning(false);
    }
  }

  return (
    <main className="container-app min-h-screen pt-10">
      <div className="relative isolate overflow-hidden rounded-3xl p-7 text-white shadow-card sm:p-9">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/fuji-sakura.jpg" alt="" className="absolute inset-0 -z-20 h-full w-full object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-900/94 via-indigo-900/90 to-sakura-600/70" />
        <span className="eyebrow text-sakura-300">Build my plan</span>
        <h1 className="mt-2 font-display text-3xl font-bold sm:text-4xl">Your personal migration plan, in one run.</h1>
        <p className="mt-2 max-w-2xl text-white/80">
          Tell us about you — or upload your resume. Autonomous agents read official Japanese sources + live jobs to
          build a cited, personalized plan. Pick your language, then watch them work live.
        </p>
        <div className="mt-4 flex flex-wrap gap-2 text-xs">
          {["Real data only", "Every claim cited", "EN · हिन्दी · 日本語", "Free"].map((t) => (
            <span key={t} className="glass px-3 py-1 font-medium text-white/85">{t}</span>
          ))}
        </div>
      </div>

      <div className="mt-8 grid items-start gap-6 lg:grid-cols-2">
        <IntakeForm onRun={handleRun} loading={running} />
        <AgentTimeline steps={steps} running={running} />
      </div>

      {error && <div className="card mt-6 border-red-200 bg-red-50 text-sm text-red-700">⚠️ {error}</div>}
      {result && <div className="mt-10"><ResultsPanel result={result} profile={profile} /></div>}
    </main>
  );
}
