"use client";

import { motion } from "framer-motion";
import { ArrowDown, ShieldCheck, Sparkles } from "lucide-react";

const STATS = [
  { value: "50,000", label: "Indian workers → Japan (2025 pact)" },
  { value: "19", label: "eligible SSW sectors" },
  { value: "0", label: "hallucinations (grounded)" },
];

export function Hero() {
  return (
    <header className="relative overflow-hidden">
      {/* Ambient gradient + Mt. Fuji silhouette */}
      <div className="pointer-events-none absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-b from-sakura-50 via-white to-[#fbf9fb]" />
        <div className="absolute -right-10 top-10 h-40 w-40 rounded-full bg-sakura-300/30 blur-3xl" />
        <div className="absolute left-0 top-24 h-40 w-40 rounded-full bg-indigo-700/10 blur-3xl" />
        <svg viewBox="0 0 1200 300" className="absolute bottom-0 w-full opacity-[0.13]" preserveAspectRatio="none">
          <path d="M0 300 L470 70 L560 150 L640 70 L1200 300 Z" fill="#2b2d6e" />
          <path d="M440 100 L470 70 L500 100 L485 112 L470 104 L455 112 Z" fill="#fff" />
        </svg>
        {/* floating petals */}
        {[12, 28, 55, 78, 90].map((x, i) => (
          <motion.span
            key={i}
            className="absolute text-sakura-300"
            style={{ left: `${x}%`, top: `${10 + i * 6}%` }}
            animate={{ y: [0, 18, 0], rotate: [0, 25, 0], opacity: [0.5, 0.9, 0.5] }}
            transition={{ duration: 6 + i, repeat: Infinity, ease: "easeInOut" }}
          >
            ❀
          </motion.span>
        ))}
      </div>

      <div className="container-app pb-10 pt-16 sm:pt-24">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <span className="chip">
            <Sparkles className="h-3.5 w-3.5" /> Agentic &amp; Autonomous Systems · FAR AWAY 2026
          </span>

          <h1 className="mt-5 font-display text-5xl leading-[1.05] tracking-tight sm:text-7xl">
            <span className="text-bridge">Kakehashi</span>{" "}
            <span className="align-middle text-3xl text-ink/40 sm:text-4xl">架け橋</span>
          </h1>

          <p className="mt-5 max-w-2xl text-lg text-ink/70 sm:text-xl">
            An autonomous, <span className="font-semibold text-ink">source-grounded</span> multi-agent
            system that bridges Indian skilled workers into Japan&apos;s{" "}
            <span className="font-semibold text-ink">Specified Skilled Worker</span> program — every
            answer cited from official sources, every claim measured.
          </p>

          <div className="mt-7 flex flex-wrap items-center gap-3">
            <a href="#start" className="btn-primary">
              Build my migration plan <ArrowDown className="h-4 w-4" />
            </a>
            <span className="inline-flex items-center gap-2 text-sm text-ink/60">
              <ShieldCheck className="h-4 w-4 text-emerald-600" /> Real data only — never fabricated
            </span>
          </div>

          <div className="mt-12 grid max-w-2xl grid-cols-3 gap-4">
            {STATS.map((s) => (
              <div key={s.label} className="card !p-4">
                <div className="font-display text-3xl text-bridge">{s.value}</div>
                <div className="mt-1 text-xs text-ink/60">{s.label}</div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </header>
  );
}
