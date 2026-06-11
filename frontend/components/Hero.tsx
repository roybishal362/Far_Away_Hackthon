"use client";

import { motion } from "framer-motion";
import { ArrowRight, ShieldCheck, Sparkles } from "lucide-react";

const STATS = [
  { value: "50,000", label: "skilled Indians → Japan (2025 pact)" },
  { value: "0", label: "hallucinations, grounded" },
  { value: "EN·हि·日", label: "answers in your language" },
];

const PETALS = [8, 22, 38, 60, 74, 88];

export function Hero() {
  return (
    <header className="relative isolate overflow-hidden">
      {/* full-bleed photograph */}
      <div className="absolute inset-0 -z-20">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src="/images/sakura.jpg"
          alt="Mount Fuji framed by cherry blossoms"
          className="h-full w-full object-cover object-center"
        />
      </div>
      {/* legibility scrims */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-r from-white via-white/90 to-white/20 sm:to-transparent" />
      <div className="absolute inset-0 -z-10 bg-gradient-to-t from-[#fbf9fb] via-transparent to-white/40" />

      {/* floating petals */}
      <div className="pointer-events-none absolute inset-0 -z-10">
        {PETALS.map((x, i) => (
          <motion.span
            key={i}
            className="absolute text-sakura-300/80"
            style={{ left: `${x}%`, top: `${6 + i * 9}%`, fontSize: `${14 + (i % 3) * 6}px` }}
            animate={{ y: [0, 22, 0], x: [0, 10, 0], rotate: [0, 30, 0], opacity: [0.4, 0.85, 0.4] }}
            transition={{ duration: 7 + i, repeat: Infinity, ease: "easeInOut" }}
          >
            ❀
          </motion.span>
        ))}
      </div>

      <div className="container-app pb-20 pt-16 sm:pb-28 sm:pt-24">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65 }}
          className="max-w-2xl"
        >
          <span className="chip shadow-sm">
            <Sparkles className="h-3.5 w-3.5" /> Agentic &amp; Autonomous Systems · FAR AWAY 2026
          </span>

          <h1 className="mt-5 font-display text-[2.7rem] font-extrabold leading-[1.03] tracking-tight sm:text-7xl">
            Your bridge to a<br className="hidden sm:block" /> life in <span className="text-bridge">Japan</span>.
          </h1>

          <p className="mt-5 max-w-xl text-lg text-ink/75 sm:text-xl">
            <b className="text-ink">Kakehashi</b> <span className="text-ink/50">架け橋</span> is an autonomous,
            source-grounded AI guide for Indian skilled workers. It finds your visa path, ranks{" "}
            <span className="font-semibold text-ink">real jobs</span>, and cites every fact from official
            Japanese sources.
          </p>

          <div className="mt-7 flex flex-wrap items-center gap-3">
            <a href="/app" className="btn-primary text-base">
              Build my migration plan <ArrowRight className="h-4 w-4" />
            </a>
            <a href="/how" className="btn-ghost">
              See how it works
            </a>
          </div>
          <div className="mt-3 inline-flex items-center gap-2 text-sm text-ink/55">
            <ShieldCheck className="h-4 w-4 text-emerald-600" /> Real data only — never fabricated
          </div>

          <div className="mt-10 grid max-w-xl grid-cols-3 gap-3">
            {STATS.map((s) => (
              <div
                key={s.label}
                className="rounded-2xl border border-black/[0.06] bg-white/70 p-4 shadow-card backdrop-blur"
              >
                <div className="font-display text-2xl font-bold text-bridge sm:text-3xl">{s.value}</div>
                <div className="mt-1 text-[11px] leading-tight text-ink/60">{s.label}</div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </header>
  );
}
