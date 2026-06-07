import { EvalReport, Profile, RunResult, StepEvent } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface StreamHandlers {
  onStart?: (d: { agents: string[] }) => void;
  onStep?: (s: StepEvent) => void;
  onResult?: (r: RunResult) => void;
  onError?: (e: { message: string }) => void;
}

/** POST-based SSE: fetch + manual parse (EventSource only supports GET). */
export async function streamRun(profile: Profile, h: StreamHandlers, signal?: AbortSignal): Promise<void> {
  const res = await fetch(`${API}/run/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
    signal,
  });
  if (!res.ok || !res.body) {
    throw new Error(res.status === 422 ? "Please check your inputs and try again." : `Run failed: ${res.status}`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";
    for (const part of parts) {
      let event = "message";
      let data = "";
      for (const line of part.split("\n")) {
        if (line.startsWith("event:")) event = line.slice(6).trim();
        else if (line.startsWith("data:")) data += line.slice(5).trim();
      }
      if (!data) continue;
      let parsed: any;
      try {
        parsed = JSON.parse(data);
      } catch {
        continue;
      }
      if (event === "start") h.onStart?.(parsed);
      else if (event === "step") h.onStep?.(parsed);
      else if (event === "result") h.onResult?.(parsed);
      else if (event === "error") h.onError?.(parsed);
    }
  }
}

export async function runEval(profile: Profile): Promise<EvalReport> {
  const res = await fetch(`${API}/eval`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  if (!res.ok) throw new Error(`Eval failed: ${res.status}`);
  return res.json();
}

export async function getHealth(): Promise<any> {
  const res = await fetch(`${API}/health`);
  return res.json();
}

export async function chat(
  question: string,
  profile: Profile | null,
  history: { role: string; content: string }[]
): Promise<{ answer: string; citations: { url: string; title: string }[] }> {
  const res = await fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, profile, history }),
  });
  if (!res.ok) throw new Error("Chat failed");
  return res.json();
}

export async function uploadResume(file: File): Promise<Partial<Profile>> {
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(`${API}/resume`, { method: "POST", body: fd });
  if (!res.ok) throw new Error("Resume parse failed");
  return res.json();
}

export async function savePlan(plan: RunResult, profile: Profile | null): Promise<{ id: string }> {
  const res = await fetch(`${API}/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ result: plan, profile }),
  });
  if (!res.ok) throw new Error("Save failed");
  return res.json();
}

export async function loadPlan(id: string): Promise<{ result: RunResult; profile: Profile | null }> {
  const res = await fetch(`${API}/plan/${id}`);
  if (!res.ok) throw new Error("Plan not found");
  const data = await res.json();
  // New shape {result, profile}; tolerate a legacy bare RunResult.
  if (data && data.result) return { result: data.result, profile: data.profile ?? null };
  return { result: data, profile: null };
}

export async function downloadDossier(plan: RunResult, profile: Profile | null): Promise<void> {
  const res = await fetch(`${API}/dossier`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plan, profile }),
  });
  if (!res.ok) throw new Error("PDF failed");
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "kakehashi-dossier.pdf";
  a.click();
  URL.revokeObjectURL(url);
}
