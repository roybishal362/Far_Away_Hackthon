"use client";

import { useEffect, useState } from "react";
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
    <main className="container-app min-h-screen pt-10">
      <div className="mb-6">
        <h1 className="font-display text-3xl sm:text-4xl">Build your migration plan</h1>
        <p className="mt-1 max-w-2xl text-ink/60">
          Tell us about you — autonomous agents read official Japanese sources + live jobs to build a cited,
          personalized plan. Upload your resume to auto-fill, and pick your language.
        </p>
      </div>

      <div className="grid items-start gap-6 lg:grid-cols-2">
        <IntakeForm onRun={handleRun} loading={running} />
        <AgentTimeline steps={steps} running={running} />
      </div>

      {error && <div className="card mt-6 border-red-200 bg-red-50 text-sm text-red-700">⚠️ {error}</div>}
      {result && <div className="mt-10"><ResultsPanel result={result} profile={profile} /></div>}
    </main>
  );
}
