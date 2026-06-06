import { EvalReport, Profile, RunResult, StepEvent } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface StreamHandlers {
  onStart?: (d: { agents: string[] }) => void;
  onStep?: (s: StepEvent) => void;
  onResult?: (r: RunResult) => void;
  onError?: (e: { message: string }) => void;
}

/** POST-based SSE: fetch + manual parse (EventSource only supports GET). */
export async function streamRun(profile: Profile, h: StreamHandlers): Promise<void> {
  const res = await fetch(`${API}/run/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  if (!res.ok || !res.body) throw new Error(`Run failed: ${res.status}`);

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
