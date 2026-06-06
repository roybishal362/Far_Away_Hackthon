"use client";

import { useState } from "react";
import { BarChart, Bar, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { AlertTriangle, FlaskConical, Loader2 } from "lucide-react";
import { runEval } from "@/lib/api";
import { EvalReport, Profile } from "@/lib/types";

export function ProofDashboard({ profile }: { profile: Profile | null }) {
  const [report, setReport] = useState<EvalReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    if (!profile) return;
    setLoading(true);
    setError(null);
    try {
      setReport(await runEval(profile));
    } catch (e: any) {
      setError(e.message ?? "Eval failed");
    } finally {
      setLoading(false);
    }
  }

  const accuracyData = report
    ? [
        { name: "Our agents (grounded)", value: Math.round(report.grounded_accuracy * 100), fill: "#10b981" },
        { name: "Plain LLM (ungrounded)", value: Math.round(report.ungrounded_accuracy * 100), fill: "#f43f6e" },
      ]
    : [];

  return (
    <div className="card">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="flex items-center gap-2 font-display text-2xl">
            <FlaskConical className="h-6 w-6 text-sakura-600" /> The proof
          </h3>
          <p className="mt-1 text-sm text-ink/60">
            Same question, two ways — grounded in official sources vs. a plain LLM. Measured against{" "}
            {report?.gold_n ?? 7} gold facts.
          </p>
        </div>
        <button className="btn-ghost" onClick={run} disabled={loading || !profile}>
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <FlaskConical className="h-4 w-4" />}
          Run ablation
        </button>
      </div>

      {error && <p className="mt-4 text-sm text-red-600">⚠️ {error}</p>}
      {!profile && !report && (
        <p className="mt-6 text-sm text-ink/40">Run the agents first, then prove the results here.</p>
      )}

      {report && (
        <div className="mt-6 grid gap-6 sm:grid-cols-2">
          <div>
            <p className="mb-2 text-sm font-medium text-ink/70">Factual accuracy (% of gold facts correct)</p>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={accuracyData} layout="vertical" margin={{ left: 8, right: 24 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" domain={[0, 100]} unit="%" fontSize={12} />
                <YAxis type="category" dataKey="name" width={120} fontSize={11} />
                <Tooltip formatter={(v) => `${v}%`} />
                <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                  {accuracyData.map((d, i) => (
                    <Cell key={i} fill={d.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="flex flex-col justify-center gap-3">
            <p className="text-sm font-medium text-ink/70">
              <AlertTriangle className="mr-1 inline h-4 w-4 text-amber-500" /> Hallucinations (claims contradicting official facts)
            </p>
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-xl bg-emerald-50 p-4 text-center">
                <div className="font-display text-4xl text-emerald-700">{report.grounded_hallucinations}</div>
                <div className="text-xs text-emerald-700/80">Our agents</div>
              </div>
              <div className="rounded-xl bg-sakura-50 p-4 text-center">
                <div className="font-display text-4xl text-sakura-600">{report.ungrounded_hallucinations}</div>
                <div className="text-xs text-sakura-600/80">Plain LLM</div>
              </div>
            </div>
            <p className="text-xs text-ink/50">
              Grounding lifts accuracy {Math.round(report.ungrounded_accuracy * 100)}% →{" "}
              {Math.round(report.grounded_accuracy * 100)}% and cuts hallucinations to{" "}
              {report.grounded_hallucinations}.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
