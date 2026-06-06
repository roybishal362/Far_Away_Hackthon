import { ExternalLink } from "lucide-react";
import { Citation } from "@/lib/types";

export function CitationBadge({ c }: { c: Citation }) {
  return (
    <a
      href={c.url}
      target="_blank"
      rel="noreferrer"
      title={c.snippet || c.title}
      className="group inline-flex max-w-full items-center gap-1.5 rounded-lg border border-indigo-800/15
                 bg-indigo-800/[0.04] px-2.5 py-1 text-xs text-indigo-800 transition hover:bg-indigo-800/[0.09]"
    >
      <span className="truncate">{c.title}</span>
      <ExternalLink className="h-3 w-3 shrink-0 opacity-60 group-hover:opacity-100" />
    </a>
  );
}

export function CitationRow({ citations }: { citations: Citation[] }) {
  if (!citations?.length) return null;
  return (
    <div className="mt-4 border-t border-black/[0.06] pt-3">
      <p className="mb-2 text-[11px] font-semibold uppercase tracking-wide text-ink/40">
        Sources ({citations.length})
      </p>
      <div className="flex flex-wrap gap-1.5">
        {citations.map((c, i) => (
          <CitationBadge key={i} c={c} />
        ))}
      </div>
    </div>
  );
}
