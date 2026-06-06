"use client";

import { useMemo, useState } from "react";
import {
  Briefcase, CalendarClock, CheckCircle2, ExternalLink, FileText, GraduationCap,
  MapPin, Search, ShieldCheck, Sparkles, AlertTriangle, Plane, BookOpen,
} from "lucide-react";
import { AgentResult, Profile, RunResult } from "@/lib/types";
import { CitationRow } from "./Citation";
import { ProofDashboard } from "./ProofDashboard";

/* ---------- shared ---------- */

function Pill({ children, tone = "slate" }: { children: React.ReactNode; tone?: string }) {
  const tones: Record<string, string> = {
    green: "bg-emerald-50 text-emerald-700",
    amber: "bg-amber-50 text-amber-700",
    red: "bg-red-50 text-red-600",
    indigo: "bg-indigo-800/10 text-indigo-800",
    slate: "bg-black/[0.05] text-ink/70",
  };
  return <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${tones[tone]}`}>{children}</span>;
}

function ReadinessBar({ pct }: { pct: number }) {
  const tone = pct >= 70 ? "#10b981" : pct >= 45 ? "#ff9500" : "#f43f6e";
  return (
    <div>
      <div className="mb-1 flex items-baseline justify-between">
        <span className="text-sm font-medium text-ink/70">Readiness</span>
        <span className="font-display text-2xl" style={{ color: tone }}>{pct}%</span>
      </div>
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-black/[0.06]">
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: tone }} />
      </div>
    </div>
  );
}

/* ---------- Pathway ---------- */

function PathwayTab({ r }: { r?: AgentResult }) {
  if (!r?.ok) return <Empty msg="Pathway unavailable." />;
  const d = r.data || {};

  if (d.eligibility_verdict === "redirect" && d.non_ssw) {
    return (
      <div className="card border-indigo-800/20">
        <Pill tone="indigo"><Sparkles className="h-3 w-3" /> Correct route</Pill>
        <h4 className="mt-2 font-display text-2xl">{d.non_ssw.name} → {d.non_ssw.verdict}</h4>
        <p className="mt-2 text-sm text-ink/75">{d.non_ssw.detail}</p>
        <CitationRow citations={r.citations} />
      </div>
    );
  }

  const verdict: string = d.eligibility_verdict || "assessed";
  const vtone = verdict.startsWith("eligible") && !verdict.includes("gaps") ? "green" : verdict.includes("gaps") ? "amber" : "red";
  return (
    <div className="grid gap-5 lg:grid-cols-2">
      <div className="card">
        <div className="mb-3 flex items-center justify-between">
          <h4 className="flex items-center gap-2 font-display text-xl"><MapPin className="h-5 w-5 text-sakura-600" /> Your verdict</h4>
          <Pill tone={vtone}>{verdict}</Pill>
        </div>
        {typeof d.readiness_percent === "number" && <ReadinessBar pct={d.readiness_percent} />}
        {r.summary && <p className="mt-3 text-sm text-ink/75">{r.summary}</p>}
        {d.timeline && <p className="mt-3 text-sm"><CalendarClock className="mr-1 inline h-4 w-4 text-indigo-700" /><b>Timeline:</b> {d.timeline}</p>}
        {!!(d.recommended_sectors || []).length && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {d.recommended_sectors.map((s: any, i: number) => <Pill key={i} tone="slate">{s.sector}{s.fit ? ` · ${s.fit}` : ""}</Pill>)}
          </div>
        )}
        <CitationRow citations={r.citations} />
      </div>

      <div className="space-y-5">
        {!!(d.what_you_have || []).length && (
          <div className="card">
            <h4 className="mb-2 flex items-center gap-2 font-display text-lg text-emerald-700"><CheckCircle2 className="h-5 w-5" /> What you have</h4>
            <ul className="space-y-1.5 text-sm text-ink/80">{d.what_you_have.map((x: string, i: number) => <li key={i}>✅ {x}</li>)}</ul>
          </div>
        )}
        {!!(d.what_you_need || []).length && (
          <div className="card">
            <h4 className="mb-2 flex items-center gap-2 font-display text-lg text-amber-700"><AlertTriangle className="h-5 w-5" /> What you need</h4>
            <ul className="space-y-1.5 text-sm text-ink/80">{d.what_you_need.map((x: string, i: number) => <li key={i}>• {x}</li>)}</ul>
          </div>
        )}
      </div>
    </div>
  );
}

/* ---------- Jobs (searchable, comprehensive) ---------- */

function JobsTab({ r }: { r?: AgentResult }) {
  const [q, setQ] = useState("");
  if (!r?.ok) return <Empty msg={r?.error ? `Jobs: ${r.error}` : "Jobs unavailable."} />;
  const jobs: any[] = r.data?.jobs || [];
  const filtered = useMemo(
    () => jobs.filter((j) => `${j.title} ${j.employer} ${j.city}`.toLowerCase().includes(q.toLowerCase())),
    [jobs, q]
  );
  return (
    <div className="card">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h4 className="flex items-center gap-2 font-display text-xl"><Briefcase className="h-5 w-5 text-indigo-700" /> {jobs.length} live openings</h4>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink/40" />
          <input className="input !w-64 pl-9" placeholder="Filter by title / employer / city" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
      </div>
      <div className="grid max-h-[480px] gap-2 overflow-auto pr-1 sm:grid-cols-2">
        {filtered.map((j, i) => (
          <a key={i} href={j.apply_link} target="_blank" rel="noreferrer"
            className="group flex items-center justify-between gap-3 rounded-lg border border-black/[0.06] p-3 transition hover:border-sakura-300 hover:bg-sakura-50/40">
            <div className="min-w-0">
              <p className="truncate text-sm font-medium text-ink">{j.title}</p>
              <p className="truncate text-xs text-ink/55">{j.employer}{j.city ? ` · ${j.city}` : ""}{j.employment_type ? ` · ${j.employment_type}` : ""}</p>
            </div>
            <ExternalLink className="h-4 w-4 shrink-0 text-ink/30 group-hover:text-sakura-600" />
          </a>
        ))}
        {!filtered.length && <p className="py-6 text-sm text-ink/40">No matches for “{q}”.</p>}
      </div>
      <CitationRow citations={r.citations} />
    </div>
  );
}

/* ---------- Procedure (real links per step) ---------- */

function ProcedureTab({ r }: { r?: AgentResult }) {
  if (!r?.ok) return <Empty msg="Procedure unavailable." />;
  const d = r.data || {};
  const steps: any[] = d.steps || [];
  return (
    <div className="space-y-4">
      {d.summary && <div className="card text-sm text-ink/75">{d.summary}</div>}
      {d.skills_test && (
        <div className="card border-marigold-400/30 bg-marigold-400/[0.06]">
          <p className="text-sm"><b>Your sector skills test:</b> {d.skills_test.test_name}</p>
          <p className="mt-1 text-xs text-ink/60">Administered by {d.skills_test.administrator}.{" "}
            <a className="text-indigo-800 underline" href={d.skills_test.register_url} target="_blank" rel="noreferrer">Register →</a>
          </p>
        </div>
      )}
      {steps.map((s, i) => (
        <div key={i} className="card">
          <div className="flex items-start gap-3">
            <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-indigo-800 text-sm font-semibold text-white">{i + 1}</span>
            <div className="min-w-0 flex-1">
              <h5 className="font-medium text-ink">{s.step}</h5>
              {s.detail && <p className="mt-1 text-sm text-ink/70">{s.detail}</p>}
              {!!(s.resources || []).length && (
                <div className="mt-3 space-y-1.5">
                  {s.resources.map((res: any, k: number) => (
                    <a key={k} href={res.url} target="_blank" rel="noreferrer"
                      className="group flex items-start gap-2 rounded-lg bg-black/[0.02] p-2 transition hover:bg-indigo-800/[0.05]">
                      <ExternalLink className="mt-0.5 h-3.5 w-3.5 shrink-0 text-indigo-700" />
                      <span className="text-xs"><b className="text-ink">{res.name}</b> — <span className="text-ink/60">{res.purpose}</span></span>
                    </a>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
      <CitationRow citations={r.citations} />
    </div>
  );
}

/* ---------- Study plan + resources ---------- */

function StudyTab({ r }: { r?: AgentResult }) {
  if (!r?.ok) return <Empty msg="Study plan unavailable." />;
  const d = r.data || {};
  return (
    <div className="grid gap-5 lg:grid-cols-2">
      <div className="card">
        <h4 className="mb-3 flex items-center gap-2 font-display text-xl"><GraduationCap className="h-5 w-5 text-emerald-700" /> Your study plan</h4>
        {r.summary && <p className="mb-3 text-sm text-ink/70">{r.summary}</p>}
        {!!(d.gaps || []).length && (
          <div className="mb-3 flex flex-wrap gap-1.5">{d.gaps.map((g: string, i: number) => <Pill key={i} tone="amber">Gap: {g}</Pill>)}</div>
        )}
        <div className="space-y-2">
          {(d.plan || []).map((m: any, i: number) => (
            <div key={i} className="flex items-center gap-3 rounded-lg bg-black/[0.02] p-2.5">
              <span className="rounded-md bg-emerald-600 px-2 py-1 text-xs font-semibold text-white">{m.weeks}w</span>
              <div><p className="text-sm font-medium text-ink">{m.milestone}</p>{m.detail && <p className="text-xs text-ink/55">{m.detail}</p>}</div>
            </div>
          ))}
        </div>
      </div>
      <div className="card">
        <h4 className="mb-3 flex items-center gap-2 font-display text-xl"><BookOpen className="h-5 w-5 text-sakura-600" /> Free resources</h4>
        <div className="space-y-2">
          {(d.resources || []).map((res: any, i: number) => (
            <a key={i} href={res.url} target="_blank" rel="noreferrer"
              className="group block rounded-lg border border-black/[0.06] p-3 transition hover:border-sakura-300 hover:bg-sakura-50/40">
              <div className="flex items-center justify-between gap-2">
                <span className="text-sm font-medium text-ink">{res.name}</span>
                {res.level && <Pill tone="slate">{res.level}</Pill>}
              </div>
              <p className="mt-0.5 text-xs text-ink/55">{res.purpose}</p>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ---------- Proof tab ---------- */

function ProofTab({ result, profile }: { result: RunResult; profile: Profile | null }) {
  const agents = Object.values(result.results).filter((a) => a.ok);
  return (
    <div className="space-y-5">
      <div className="card">
        <h4 className="mb-3 flex items-center gap-2 font-display text-xl"><ShieldCheck className="h-5 w-5 text-emerald-600" /> Per-agent grounding</h4>
        <div className="space-y-2">
          {agents.map((a) => (
            <div key={a.agent} className="flex items-center gap-3">
              <span className="w-24 shrink-0 text-sm capitalize text-ink/70">{a.agent}</span>
              <div className="h-2 flex-1 overflow-hidden rounded-full bg-black/[0.06]">
                <div className="h-full rounded-full bg-emerald-500" style={{ width: `${Math.round(a.confidence * 100)}%` }} />
              </div>
              <Pill tone={a.grounded ? "green" : "amber"}>{a.grounded ? "cited" : "—"} · {a.citations.length}</Pill>
            </div>
          ))}
        </div>
      </div>
      <ProofDashboard profile={profile} />
    </div>
  );
}

/* ---------- shell ---------- */

function Empty({ msg }: { msg: string }) {
  return <div className="card text-sm text-ink/50">{msg}</div>;
}

export function ResultsPanel({ result, profile }: { result: RunResult; profile: Profile | null }) {
  const [tab, setTab] = useState("pathway");
  const r = result.results;
  const tabs = [
    { id: "pathway", label: "Pathway", icon: <MapPin className="h-4 w-4" /> },
    { id: "jobs", label: `Jobs (${r.jobs?.data?.jobs?.length ?? 0})`, icon: <Briefcase className="h-4 w-4" /> },
    { id: "procedure", label: "Procedure", icon: <FileText className="h-4 w-4" /> },
    { id: "study", label: "Study plan", icon: <GraduationCap className="h-4 w-4" /> },
    { id: "journey", label: "Journey", icon: <Plane className="h-4 w-4" /> },
    { id: "proof", label: "Proof", icon: <ShieldCheck className="h-4 w-4" /> },
  ];

  return (
    <div>
      {/* trust banner */}
      <div className="card mb-5 flex flex-wrap items-center justify-between gap-4 bg-gradient-to-r from-indigo-800 to-sakura-600 text-white">
        <div>
          <p className="text-sm opacity-80">System trust score</p>
          <p className="font-display text-4xl">{Math.round(result.grounding_score * 100)}%</p>
          <p className="text-xs opacity-80">of agent answers grounded in official sources</p>
        </div>
        <ShieldCheck className="h-12 w-12 opacity-80" />
      </div>

      {/* tab bar */}
      <div className="mb-5 flex flex-wrap gap-1.5 rounded-2xl border border-black/[0.06] bg-white/70 p-1.5 backdrop-blur">
        {tabs.map((t) => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={"inline-flex items-center gap-1.5 rounded-xl px-3.5 py-2 text-sm font-medium transition " +
              (tab === t.id ? "bg-gradient-to-r from-sakura-600 to-marigold-500 text-white shadow-glow" : "text-ink/60 hover:bg-black/[0.04]")}>
            {t.icon}{t.label}
          </button>
        ))}
      </div>

      {tab === "pathway" && <PathwayTab r={r.pathway} />}
      {tab === "jobs" && <JobsTab r={r.jobs} />}
      {tab === "procedure" && <ProcedureTab r={r.procedure} />}
      {tab === "study" && <StudyTab r={r.prep} />}
      {tab === "journey" && <JourneyRoadmap />}
      {tab === "proof" && <ProofTab result={result} profile={profile} />}
    </div>
  );
}

function JourneyRoadmap() {
  return (
    <div className="card relative overflow-hidden">
      <span className="absolute right-4 top-4 rounded-full bg-indigo-800/10 px-2.5 py-0.5 text-[11px] font-semibold text-indigo-800">Round 2</span>
      <h4 className="flex items-center gap-2 font-display text-xl"><Plane className="h-5 w-5 text-indigo-700" /> Journey &amp; relocation</h4>
      <p className="mt-2 text-sm text-ink/70">
        Real flight offers, cost &amp; timeline planning (Amadeus integration is built and wired) — launching in Round 2.
        The agent and tool are production-ready; only the paid data tier is pending.
      </p>
      <div className="mt-4 flex items-center gap-2 text-xs text-ink/45"><Sparkles className="h-4 w-4" /> Architecture ready · plug-and-play</div>
    </div>
  );
}
