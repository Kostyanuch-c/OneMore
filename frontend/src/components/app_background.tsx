import type { ReactNode } from "react";

export default function AppBackground({ children }: { children: ReactNode }) {
  return (
    <div className="relative min-h-screen bg-background">
      <div className="pointer-events-none fixed inset-0 z-0 hidden dark:block dark:bg-[radial-gradient(circle_at_50%_0%,rgba(59,130,246,0.22),transparent_38%),radial-gradient(circle_at_8%_35%,rgba(14,165,233,0.14),transparent_32%),radial-gradient(circle_at_92%_60%,rgba(59,130,246,0.14),transparent_30%)]" />

      <div className="relative z-10">{children}</div>
    </div>
  );
}
