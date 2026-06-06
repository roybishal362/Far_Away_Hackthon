import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Japan x India bridge palette
        sakura: { 50: "#fff5f7", 100: "#ffe3ea", 300: "#ff9bb3", 500: "#f43f6e", 600: "#e11d54" },
        indigo: { 700: "#2b2d6e", 800: "#1f2150", 900: "#15163a" },
        marigold: { 400: "#ffb031", 500: "#ff9500", 600: "#e07b00" },
        ink: "#15163a",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        display: ["var(--font-display)", "Georgia", "serif"],
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(244,63,110,.12), 0 12px 40px -12px rgba(43,45,110,.25)",
        card: "0 1px 2px rgba(21,22,58,.04), 0 8px 30px -12px rgba(21,22,58,.15)",
      },
      keyframes: {
        shimmer: { "100%": { transform: "translateX(100%)" } },
        float: { "0%,100%": { transform: "translateY(0)" }, "50%": { transform: "translateY(-8px)" } },
      },
      animation: { shimmer: "shimmer 1.6s infinite", float: "float 6s ease-in-out infinite" },
    },
  },
  plugins: [],
};

export default config;
