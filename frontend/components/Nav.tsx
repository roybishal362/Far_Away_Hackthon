"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ArrowRight } from "lucide-react";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/how", label: "How it works" },
];

export function Nav() {
  const path = usePathname();
  return (
    <nav className="sticky top-0 z-50 border-b border-black/[0.06] bg-white/70 backdrop-blur-md">
      <div className="container-app flex h-16 items-center justify-between">
        <Link href="/" className="font-display text-xl">
          <span className="text-bridge">Kakehashi</span>{" "}
          <span className="align-middle text-sm text-ink/40">架け橋</span>
        </Link>
        <div className="flex items-center gap-1">
          {LINKS.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className={"rounded-lg px-3 py-2 text-sm font-medium transition " + (path === l.href ? "text-ink" : "text-ink/55 hover:text-ink")}
            >
              {l.label}
            </Link>
          ))}
          <Link href="/app" className="btn-primary !px-4 !py-2 text-sm">
            Build my plan <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    </nav>
  );
}
