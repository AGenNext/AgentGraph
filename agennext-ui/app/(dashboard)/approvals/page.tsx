// app/(dashboard)/approvals/page.tsx
"use client";

import { useState, useEffect, useCallback } from "react";
import { listPendingApprovals } from "@/lib/a2a-client";
import { ApprovalPanel } from "@/components/ApprovalPanel";
import type { ApprovalRequest } from "@/types/a2a";

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(() => {
    listPendingApprovals()
      .then(setApprovals)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    refresh();
    // Poll every 10s for new approvals
    const interval = setInterval(refresh, 10000);
    return () => clearInterval(interval);
  }, [refresh]);

  const handleResponded = (taskId: string) => {
    setApprovals((prev) => prev.filter((a) => a.taskId !== taskId));
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "#F9FAFB",
      fontFamily: "'DM Sans', -apple-system, sans-serif",
    }}>
      <nav style={{
        background: "white",
        borderBottom: "1px solid #E5E7EB",
        padding: "0 32px",
        height: 56,
        display: "flex",
        alignItems: "center",
        gap: 16,
      }}>
        <a href="/" style={{ fontSize: 13, color: "#6B7280", textDecoration: "none" }}>← Back</a>
        <span style={{ fontWeight: 600, fontSize: 15, color: "#111827" }}>Approvals</span>
        {approvals.length > 0 && (
          <span style={{
            padding: "2px 8px", borderRadius: 999,
            background: "#FEF3C7", color: "#D97706",
            fontSize: 12, fontWeight: 600,
          }}>
            {approvals.length} pending
          </span>
        )}
      </nav>

      <div style={{ maxWidth: 680, margin: "0 auto", padding: "40px 24px" }}>
        <h1 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 700, color: "#111827" }}>
          Pending approvals
        </h1>
        <p style={{ margin: "0 0 28px", color: "#6B7280", fontSize: 14 }}>
          Agents are waiting for your input to continue.
        </p>

        {loading ? (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {[1, 2].map((i) => (
              <div key={i} style={{
                height: 140, borderRadius: 12, background: "#E5E7EB",
                animation: "shimmer 1.5s infinite",
              }} />
            ))}
          </div>
        ) : approvals.length === 0 ? (
          <div style={{
            padding: "48px 32px", textAlign: "center",
            border: "2px dashed #E5E7EB", borderRadius: 12,
            color: "#9CA3AF",
          }}>
            <div style={{ fontSize: 32, marginBottom: 8 }}>✓</div>
            <p style={{ margin: 0, fontSize: 14 }}>No pending approvals</p>
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            {approvals.map((approval) => (
              <ApprovalPanel
                key={approval.taskId}
                approval={approval}
                onResponded={() => handleResponded(approval.taskId)}
              />
            ))}
          </div>
        )}
      </div>

      <style>{`
        @keyframes shimmer {
          0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}
