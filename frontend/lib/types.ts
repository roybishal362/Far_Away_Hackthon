export interface Profile {
  skills: string;
  sector_interest: string;
  years_experience: number;
  japanese_level: string;
  education: string;
  origin_city: string;
  target_city: string;
  lang: string;
}

export interface Citation {
  url: string;
  title: string;
  snippet: string;
}

export interface AgentResult {
  agent: string;
  ok: boolean;
  error: string | null;
  summary: string;
  data: any;
  confidence: number;
  grounded: boolean;
  citations: Citation[];
}

export interface RunResult {
  grounding_score: number;
  metrics: Record<string, any>;
  results: Record<string, AgentResult>;
}

export interface StepEvent {
  agent: string;
  label: string;
  detail: string;
  kind: "think" | "tool_call" | "tool_result" | "decide" | string;
}

export interface EvalReport {
  gold_n: number;
  grounded_accuracy: number;
  ungrounded_accuracy: number;
  grounded_hallucinations: number;
  ungrounded_hallucinations: number;
}
