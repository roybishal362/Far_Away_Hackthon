"use client";

import { AnimatePresence, motion } from "framer-motion";
import { Brain, CheckCircle2, Cog, Download, Loader2, MinusCircle } from "lucide-react";
import { StepEvent } from "@/lib/types";

const AGENTS: { id: string; label: string; emoji: string }[] = [
  { id: "pathway", label: "Pathway", emoji: "🧭" },
  { id: "jobs", label: "Jobs", emoji: "💼" },
  { id: "procedure", label: "Procedure", emoji: "📄" },
  { id: "prep", label: "Prep", emoji: "📚" },
  { id: "journey", label: "Journey", emoji: "🗓️" },
];

const KIND_ICON: Record<string, JSX.Element> = {
  think: <Brain className="h-3.5 w-3.5 text-indigo-700" />,
  tool_call: <Cog className="h-3.5 w-3.5 animate-spin text-marigold-600" />,
  tool_result: <Download className="h-3.5 w-3.5 text-emerald-600" />,
  decide: <CheckCircle2 className="h-3.5 w-3.5 text-sakura-600" />,
  skip: <MinusCircle className="h-3.5 w-3.5 text-ink/30" />,
};

export function AgentTimeline({ steps, running }: { steps: StepEvent[]; running: boolean }) {
  const activeAgent = steps.length ? steps[steps.length - 1].agent : null;
  const seen = new Set(steps.map((s) => s.agent));
  const skipped = new Set(steps.filter((s) => s.kind === "skip").map((s) => s.agent));

  return (
    <div className="card">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="font-display text-2xl">Agents at work</h3>
        {running && (
          <span className="inline-flex items-center gap-2 text-sm text-ink/60">
            <Loader2 className="h-4 w-4 animate-spin" /> live
          </span>
        )}
      </div>

      {/* agent status rail */}
      <div className="mb-5 flex flex-wrap gap-2">
        {AGENTS.map((a) => {
          const isSkipped = skipped.has(a.id);
          const done = !isSkipped && seen.has(a.id) && a.id !== activeAgent;
          const active = a.id === activeAgent && running && !isSkipped;
          return (
            <span
              key={a.id}
              className={
                "inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium transition " +
                (active
                  ? "bg-marigold-500 text-white shadow-glow"
                  : done
                  ? "bg-emerald-50 text-emerald-700"
                  : isSkipped
                  ? "bg-black/[0.03] text-ink/35 line-through"
                  : "bg-black/[0.04] text-ink/40")
              }
              title={isSkipped ? "Not applicable for this visa route" : undefined}
            >
              <span className={isSkipped ? "opacity-50" : ""}>{a.emoji}</span>
              {a.label}
              {done && <CheckCircle2 className="h-3 w-3" />}
              {isSkipped && <MinusCircle className="h-3 w-3" />}
            </span>
          );
        })}
      </div>

      {/* streaming steps */}
      <div className="max-h-80 space-y-2 overflow-auto pr-1">
        <AnimatePresence initial={false}>
          {steps.map((s, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-start gap-2.5 rounded-lg bg-black/[0.02] px-3 py-2"
            >
              <span className="mt-0.5">{KIND_ICON[s.kind] ?? KIND_ICON.think}</span>
              <div className="min-w-0">
                <p className="text-sm text-ink">
                  <span className="font-semibold capitalize text-ink/50">{s.agent}</span> — {s.label}
                </p>
                {s.detail && <p className="truncate text-xs text-ink/50">{s.detail}</p>}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        {!steps.length && !running && (
          <p className="py-8 text-center text-sm text-ink/40">The agent timeline will appear here.</p>
        )}
      </div>
    </div>
  );
}
