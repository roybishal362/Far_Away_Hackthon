import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Nav } from "@/components/Nav";
import { Footer } from "@/components/Footer";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans", display: "swap" });

export const metadata: Metadata = {
  title: "Kakehashi — AI bridge for Indian workers to Japan",
  description:
    "An autonomous, source-grounded multi-agent system guiding Indian skilled workers through Japan's Specified Skilled Worker (SSW) journey — real data, cited sources, EN/HI/JA.",
  openGraph: {
    title: "Kakehashi 架け橋 — AI bridge for Indian workers to Japan",
    description: "Autonomous, source-grounded guidance through Japan's Specified Skilled Worker journey. Real jobs, official links, proof.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <Nav />
        {children}
        <Footer />
      </body>
    </html>
  );
}
