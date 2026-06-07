"use client";

import { useState } from "react";
import { Loader2, Play, Upload } from "lucide-react";
import { Profile } from "@/lib/types";
import { uploadResume } from "@/lib/api";

// Full current SSW(i) fields + the IT route + custom.
const SECTORS = [
  "Nursing Care",
  "Building Cleaning Management",
  "Industrial Product Manufacturing",
  "Construction",
  "Shipbuilding & Ship Machinery",
  "Automobile Repair & Maintenance",
  "Aviation",
  "Accommodation (Hotel/Ryokan)",
  "Road Transport (Driver)",
  "Railway",
  "Agriculture",
  "Fishery & Aquaculture",
  "Food & Beverage Manufacturing",
  "Food Service / Restaurant",
  "Forestry",
  "Wood Industry",
  "Resource Circulation / Recycling",
  "Linen Supply",
  "Logistics & Warehousing",
  "Software / IT / Engineering",
  "Other (custom)",
];
const JP_LEVELS = ["none", "JFT-Basic", "N5", "N4", "N3 or higher"];
const IN_CITIES = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Hyderabad", "Kolkata"];
const JP_CITIES = ["Tokyo", "Osaka", "Nagoya", "Fukuoka", "Sapporo"];

const LANGS = [
  { code: "en", label: "EN" },
  { code: "hi", label: "हिन्दी" },
  { code: "ja", label: "日本語" },
];

const DEFAULTS: Profile = {
  skills: "nursing, 3 years hospital experience",
  sector_interest: "Nursing Care",
  years_experience: 3,
  japanese_level: "none",
  education: "B.Sc. Nursing",
  origin_city: "Delhi",
  target_city: "Tokyo",
  lang: "en",
  resume_text: "",
};

const PERSONAS: { label: string; p: Profile }[] = [
  { label: "👩‍⚕️ Priya · Nurse", p: { ...DEFAULTS, skills: "nursing, 3 years hospital ICU", sector_interest: "Nursing Care", years_experience: 3, japanese_level: "none", education: "B.Sc Nursing", origin_city: "Delhi" } },
  { label: "👨‍💻 Arjun · Software Eng", p: { ...DEFAULTS, skills: "software developer, Python, 4 years", sector_interest: "Software / IT / Engineering", years_experience: 4, japanese_level: "N4", education: "B.Tech CSE", origin_city: "Bengaluru" } },
  { label: "🧑‍💼 Meera · HR/Recruiter", p: { ...DEFAULTS, skills: "HR generalist, recruiting, 5 years", sector_interest: "Human Resources", years_experience: 5, japanese_level: "N5", education: "MBA (HR)", origin_city: "Mumbai", target_city: "Osaka" } },
];

export function IntakeForm({ onRun, loading }: { onRun: (p: Profile) => void; loading: boolean }) {
  const [p, setP] = useState<Profile>(DEFAULTS);
  const [choice, setChoice] = useState("Nursing Care");
  const [parsing, setParsing] = useState(false);
  const set = (k: keyof Profile, v: string | number) => setP((s) => ({ ...s, [k]: v }));

  const onChoice = (v: string) => {
    setChoice(v);
    set("sector_interest", v === "Other (custom)" ? "" : v);
  };

  async function onResume(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    setParsing(true);
    try {
      const fields = await uploadResume(f);
      setP((s) => ({ ...s, ...fields }));
      if (fields.sector_interest) {
        setChoice(SECTORS.includes(fields.sector_interest) ? fields.sector_interest : "Other (custom)");
      }
    } catch {
      /* ignore — user can fill manually */
    } finally {
      setParsing(false);
    }
  }

  function usePersona(per: { p: Profile }) {
    setP(per.p);
    setChoice(SECTORS.includes(per.p.sector_interest) ? per.p.sector_interest : "Other (custom)");
    onRun(per.p);
  }

  const valid = p.skills.trim().length > 0 && (choice !== "Other (custom)" || p.sector_interest.trim().length > 0);

  return (
    <form onSubmit={(e) => { e.preventDefault(); onRun(p); }} className="card">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-display text-2xl">Tell us about you</h3>
          <p className="mt-1 text-sm text-ink/60">
            Agents read official Japanese sources + live job data to build a plan tailored to you.
          </p>
        </div>
        <div className="flex shrink-0 gap-1 rounded-xl border border-black/10 bg-white p-1" title="Output language">
          {LANGS.map((l) => (
            <button key={l.code} type="button" onClick={() => set("lang", l.code)}
              className={"rounded-lg px-2.5 py-1 text-xs font-medium transition " +
                (p.lang === l.code ? "bg-indigo-800 text-white" : "text-ink/60 hover:bg-black/[0.04]")}>
              {l.label}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-4">
        <p className="mb-2 text-xs font-medium text-ink/50">Try a sample (one click):</p>
        <div className="flex flex-wrap gap-2">
          {PERSONAS.map((per, i) => (
            <button key={i} type="button" disabled={loading} onClick={() => usePersona(per)}
              className="rounded-full border border-black/10 bg-white px-3 py-1.5 text-xs font-medium text-ink/70 transition hover:border-sakura-300 hover:bg-sakura-50/50 disabled:opacity-50">
              {per.label}
            </button>
          ))}
        </div>
      </div>

      <label className="mt-4 flex cursor-pointer items-center gap-3 rounded-xl border border-dashed border-black/15 p-3 transition hover:border-sakura-300 hover:bg-sakura-50/40">
        <input type="file" accept=".pdf,.txt" className="hidden" onChange={onResume} />
        {parsing ? <Loader2 className="h-5 w-5 animate-spin text-sakura-600" /> : <Upload className="h-5 w-5 text-sakura-600" />}
        <span className="text-sm font-medium text-ink">{parsing ? "Reading your resume…" : "Auto-fill from resume"}</span>
        <span className="text-xs text-ink/50">PDF or TXT</span>
      </label>

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        <div className="sm:col-span-2">
          <label className="label">Skills &amp; experience</label>
          <textarea className="input min-h-[72px]" value={p.skills} maxLength={400}
            onChange={(e) => set("skills", e.target.value)} placeholder="e.g. nursing, 3 years hospital experience" />
        </div>

        <div className={choice === "Other (custom)" ? "" : "sm:col-span-2"}>
          <label className="label">Sector of interest</label>
          <select className="input" value={choice} onChange={(e) => onChoice(e.target.value)}>
            {SECTORS.map((s) => <option key={s}>{s}</option>)}
          </select>
        </div>
        {choice === "Other (custom)" && (
          <div>
            <label className="label">Your sector</label>
            <input className="input" value={p.sector_interest} maxLength={80}
              onChange={(e) => set("sector_interest", e.target.value)} placeholder="Type your field" />
          </div>
        )}

        <div>
          <label className="label">Years of experience</label>
          <input type="number" min={0} step={0.5} className="input" value={p.years_experience}
            onChange={(e) => set("years_experience", Math.max(0, Number(e.target.value) || 0))} />
        </div>
        <div>
          <label className="label">Japanese level</label>
          <select className="input" value={p.japanese_level} onChange={(e) => set("japanese_level", e.target.value)}>
            {JP_LEVELS.map((s) => <option key={s}>{s}</option>)}
          </select>
        </div>
        <div>
          <label className="label">Education</label>
          <input className="input" value={p.education} maxLength={120} onChange={(e) => set("education", e.target.value)} />
        </div>
        <div>
          <label className="label">From (India)</label>
          <select className="input" value={p.origin_city} onChange={(e) => set("origin_city", e.target.value)}>
            {IN_CITIES.map((s) => <option key={s}>{s}</option>)}
          </select>
        </div>
        <div>
          <label className="label">To (Japan)</label>
          <select className="input" value={p.target_city} onChange={(e) => set("target_city", e.target.value)}>
            {JP_CITIES.map((s) => <option key={s}>{s}</option>)}
          </select>
        </div>
      </div>

      <button type="submit" className="btn-primary mt-6 w-full" disabled={loading || !valid}>
        {loading ? <><Loader2 className="h-4 w-4 animate-spin" /> Agents working…</> : <><Play className="h-4 w-4" /> Run the agents</>}
      </button>
      {!valid && <p className="mt-2 text-center text-xs text-ink/45">Add your skills{choice === "Other (custom)" ? " and sector" : ""} to continue.</p>}
    </form>
  );
}
