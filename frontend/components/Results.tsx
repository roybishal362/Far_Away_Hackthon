"use client";

import {
  Briefcase, CalendarClock, CheckCircle2, ExternalLink, FileText,
  GraduationCap, MapPin, ShieldCheck, Sparkles,
} from "lucide-react";
import { AgentResult, RunResult } from "@/lib/types";
import { CitationRow } from "./Citation";

function GroundedBadge({ r }: { r: AgentResult }) {
  return (
    <span
      className={
        "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[11px] font-medium " +
        (r.grounded ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700")
      }
    >
      <ShieldCheck className="h-3 w-3" />
      {r.grounded ? "Grounded" : "Unverified"} · {Math.round(r.confidence * 100)}%
    </span>
  );
}

function AgentCard({
  icon, title, r, children,
}: {
  icon: JSX.Element; title: string; r: AgentResult; children: React.ReactNode;
}) {
  return (
    <div className="card">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h4 className="flex items-center gap-2 font-display text-xl">{icon} {title}</h4>
        <GroundedBadge r={r} />
      </div>
      {r.summary && <p className="mb-3 text-sm text-ink/70">{r.summary}</p>}
      {children}
      <CitationRow citations={r.citations} />
    </div>
  );
}

function Pathway({ r }: { r: AgentResult }) {
  const d = r.data || {};
  return (
    <AgentCard icon={<MapPin className="h-5 w-5 text-sakura-600" />} title="Your SSW pathway" r={r}>
      {!!(d.recommended_sectors || []).length && (
        <div className="mb-3 flex flex-wrap gap-1.5">
          {d.recommended_sectors.map((s: any, i: number) => (
            <span key={i} className="chip">{s.sector}</span>
          ))}
        </div>
      )}
      {!!(d.requirements || []).length && (
        <ul className="space-y-1.5 text-sm text-ink/80">
          {d.requirements.map((req: string, i: number) => (
            <li key={i} className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />{req}</li>
          ))}
        </ul>
      )}
      {!!(d.caveats || []).length && (
        <div className="mt-3 rounded-lg bg-amber-50 p-3 text-sm text-amber-800">
          {d.caveats.map((c: string, i: number) => <p key={i}>⚠️ {c}</p>)}
        </div>
      )}
    </AgentCard>
  );
}

function Jobs({ r }: { r: AgentResult }) {
  const jobs = (r.data?.jobs || []) as any[];
  return (
    <AgentCard icon={<Briefcase className="h-5 w-5 text-indigo-700" />} title="Live job openings" r={r}>
      {jobs.length ? (
        <div className="space-y-2">
          {jobs.slice(0, 6).map((j, i) => (
            <a key={i} href={j.apply_link} target="_blank" rel="noreferrer"
               className="group flex items-center justify-between gap-3 rounded-lg border border-black/[0.06] p-3 transition hover:border-sakura-300 hover:bg-sakura-50/40">
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-ink">{j.title}</p>
                <p className="truncate text-xs text-ink/55">{j.employer}{j.city ? ` · ${j.city}` : ""}</p>
              </div>
              <ExternalLink className="h-4 w-4 shrink-0 text-ink/30 group-hover:text-sakura-600" />
            </a>
          ))}
        </div>
      ) : (
        <p className="text-sm text-ink/50">No live openings found for this query right now.</p>
      )}
    </AgentCard>
  );
}

function Procedure({ r }: { r: AgentResult }) {
  const d = r.data || {};
  return (
    <AgentCard icon={<FileText className="h-5 w-5 text-marigold-600" />} title="Step-by-step procedure" r={r}>
      <ol className="space-y-2">
        {(d.steps || []).map((s: any, i: number) => (
          <li key={i} className="flex gap-3">
            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-indigo-800 text-xs font-semibold text-white">{i + 1}</span>
            <div>
              <p className="text-sm font-medium text-ink">{s.step}</p>
              {s.detail && <p className="text-xs text-ink/55">{s.detail}</p>}
            </div>
          </li>
        ))}
      </ol>
      {!!(d.documents || []).length && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {d.documents.map((doc: string, i: number) => (
            <span key={i} className="inline-flex items-center gap-1 rounded-lg bg-black/[0.04] px-2 py-1 text-xs text-ink/70">
              <FileText className="h-3 w-3" />{doc}
            </span>
          ))}
        </div>
      )}
    </AgentCard>
  );
}

function Prep({ r }: { r: AgentResult }) {
  const d = r.data || {};
  return (
    <AgentCard icon={<GraduationCap className="h-5 w-5 text-emerald-700" />} title="Readiness & study plan" r={r}>
      {!!(d.gaps || []).length && (
        <div className="mb-3 flex flex-wrap gap-1.5">
          {d.gaps.map((g: string, i: number) => (
            <span key={i} className="inline-flex rounded-full bg-amber-50 px-2.5 py-0.5 text-xs text-amber-700">Gap: {g}</span>
          ))}
        </div>
      )}
      <div className="space-y-2">
        {(d.plan || []).map((m: any, i: number) => (
          <div key={i} className="flex items-center gap-3 rounded-lg bg-black/[0.02] p-2.5">
            <span className="rounded-md bg-emerald-600 px-2 py-1 text-xs font-semibold text-white">{m.weeks}w</span>
            <div>
              <p className="text-sm font-medium text-ink">{m.milestone}</p>
              {m.detail && <p className="text-xs text-ink/55">{m.detail}</p>}
            </div>
          </div>
        ))}
      </div>
    </AgentCard>
  );
}

function JourneyRoadmap() {
  return (
    <div className="card relative overflow-hidden">
      <span className="absolute right-4 top-4 rounded-full bg-indigo-800/10 px-2.5 py-0.5 text-[11px] font-semibold text-indigo-800">
        Round 2
      </span>
      <h4 className="flex items-center gap-2 font-display text-xl">
        <CalendarClock className="h-5 w-5 text-indigo-700" /> Journey &amp; relocation
      </h4>
      <p className="mt-2 text-sm text-ink/70">
        Real flight offers, cost &amp; timeline planning (Amadeus integration is built and wired) —
        launching in Round 2. The agent and tool are production-ready; only the paid data tier is pending.
      </p>
      <div className="mt-4 flex items-center gap-2 text-xs text-ink/45">
        <Sparkles className="h-4 w-4" /> Architecture ready · plug-and-play
      </div>
    </div>
  );
}

export function ResultsPanel({ result }: { result: RunResult }) {
  const r = result.results;
  return (
    <div>
      <div className="card mb-6 flex flex-wrap items-center justify-between gap-4 bg-gradient-to-r from-indigo-800 to-sakura-600 text-white">
        <div>
          <p className="text-sm/relaxed opacity-80">System trust score</p>
          <p className="font-display text-4xl">{Math.round(result.grounding_score * 100)}%</p>
          <p className="text-xs opacity-80">of agent answers grounded in official sources</p>
        </div>
        <ShieldCheck className="h-12 w-12 opacity-80" />
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        {r.pathway?.ok && <Pathway r={r.pathway} />}
        {r.jobs?.ok && <Jobs r={r.jobs} />}
        {r.procedure?.ok && <Procedure r={r.procedure} />}
        {r.prep?.ok && <Prep r={r.prep} />}
        <JourneyRoadmap />
      </div>
    </div>
  );
}
