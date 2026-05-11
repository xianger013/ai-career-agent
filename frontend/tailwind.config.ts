import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#1f2933",
        muted: "#667085",
        line: "#d9e2ec",
        paper: "#fbfcfe",
        accent: "#0f766e",
      },
      boxShadow: {
        card: "0 18px 45px rgba(15, 23, 42, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;

