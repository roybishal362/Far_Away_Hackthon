"use client";

import { useState } from "react";
import { Loader2, Play } from "lucide-react";
import { Profile } from "@/lib/types";

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

const DEFAULTS: Profile = {
  skills: "nursing, 3 years hospital experience",
  sector_interest: "Nursing Care",
  years_experience: 3,
  japanese_level: "none",
  education: "B.Sc. Nursing",
  origin_city: "Delhi",
  target_city: "Tokyo",
};

export function IntakeForm({ onRun, loading }: { onRun: (p: Profile) => void; loading: boolean }) {
  const [p, setP] = useState<Profile>(DEFAULTS);
  const [choice, setChoice] = useState("Nursing Care");
  const set = (k: keyof Profile, v: string | number) => setP((s) => ({ ...s, [k]: v }));

  const onChoice = (v: string) => {
    setChoice(v);
    set("sector_interest", v === "Other (custom)" ? "" : v);
  };

  return (
    <form onSubmit={(e) => { e.preventDefault(); onRun(p); }} className="card">
      <h3 className="font-display text-2xl">Tell us about you</h3>
      <p className="mt-1 text-sm text-ink/60">
        Agents read official Japanese sources + live job data to build a plan tailored to you.
      </p>

      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <div className="sm:col-span-2">
          <label className="label">Skills &amp; experience</label>
          <textarea className="input min-h-[72px]" value={p.skills}
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
            <input className="input" value={p.sector_interest}
              onChange={(e) => set("sector_interest", e.target.value)} placeholder="Type your field" />
          </div>
        )}

        <div>
          <label className="label">Years of experience</label>
          <input type="number" min={0} step={0.5} className="input" value={p.years_experience}
            onChange={(e) => set("years_experience", Number(e.target.value))} />
        </div>
        <div>
          <label className="label">Japanese level</label>
          <select className="input" value={p.japanese_level} onChange={(e) => set("japanese_level", e.target.value)}>
            {JP_LEVELS.map((s) => <option key={s}>{s}</option>)}
          </select>
        </div>
        <div>
          <label className="label">Education</label>
          <input className="input" value={p.education} onChange={(e) => set("education", e.target.value)} />
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

      <button type="submit" className="btn-primary mt-6 w-full" disabled={loading}>
        {loading ? <><Loader2 className="h-4 w-4 animate-spin" /> Agents working…</> : <><Play className="h-4 w-4" /> Run the agents</>}
      </button>
    </form>
  );
}
