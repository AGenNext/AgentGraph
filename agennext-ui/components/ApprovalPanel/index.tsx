// components/ApprovalPanel/index.tsx
"use client";

import { useState } from "react";
import { respondToApproval } from "@/lib/a2a-client";
import type { ApprovalRequest } from "@/types/a2a";

interface ApprovalPanelProps {
  approval: ApprovalRequest;
  onResponded?: () => void;
}

export function ApprovalPanel({ approval, onResponded }: ApprovalPanelProps) {
  const [loading, setLoading] = useState(false);
  const [customResponse, setCustomResponse] = useState("");
  const [responded, setResponded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const hasOptions = approval.options && approval.options.length > 0;

  const handleRespond = async (response: string) => {
    if (!response.trim()) return;
    setLoading(true);
    setError(null);
    try {
      await respondToApproval(approval.taskId, response);
      setResponded(true);
      onResponded?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to submit response");
    } finally {
      setLoading(false);
    }
  };

  const timeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return "just now";
    if (mins < 60) return `${mins}m ago`;
    return `${Math.floor(mins / 60)}h ago`;
  };

  if (responded) {
    return (
      <div style={{
        padding: "16px 20px",
        background: "#ECFDF5",
        border: "1px solid #A7F3D0",
        borderRadius: 12,
        display: "flex",
        alignItems: "center",
        gap: 10,
      }}>
        <span style={{ fontSize: 18 }}>✓</span>
        <span style={{ fontSize: 14, color: "#065F46", fontWeight: 500 }}>
          Response submitted
        </span>
      </div>
    );
  }

  return (
    <div style={{
      border: "1px solid #FDE68A",
      borderRadius: 12,
      background: "white",
      overflow: "hidden",
    }}>
      {/* Header */}
      <div style={{
        padding: "12px 16px",
        background: "#FFFBEB",
        borderBottom: "1px solid #FDE68A",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 16 }}>✋</span>
          <span style={{ fontSize: 13, fontWeight: 600, color: "#92400E" }}>
            Input Required
          </span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 12, color: "#B45309" }}>
            {approval.agentName}
          </span>
          <span style={{ fontSize: 11, color: "#D97706" }}>
            {timeAgo(approval.createdAt)}
          </span>
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: "16px 20px" }}>
        <p style={{ margin: "0 0 12px", fontSize: 14, color: "#1F2937", lineHeight: 1.6 }}>
          {approval.question}
        </p>

        {approval.context && (
          <div style={{
            padding: "10px 14px",
            background: "#F9FAFB",
            borderRadius: 8,
            marginBottom: 14,
            fontSize: 13,
            color: "#6B7280",
            lineHeight: 1.5,
          }}>
            <strong style={{ color: "#374151" }}>Context: </strong>
            {approval.context}
          </div>
        )}

        {/* Predefined options */}
        {hasOptions && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 12 }}>
            {approval.options!.map((option) => (
              <button
                key={option}
                onClick={() => handleRespond(option)}
                disabled={loading}
                style={{
                  padding: "10px 16px",
                  borderRadius: 8,
                  border: "1px solid #E5E7EB",
                  background: "white",
                  cursor: loading ? "not-allowed" : "pointer",
                  fontSize: 14,
                  color: "#374151",
                  textAlign: "left",
                  transition: "all 0.15s ease",
                  opacity: loading ? 0.6 : 1,
                }}
                onMouseEnter={(e) => {
                  (e.target as HTMLElement).style.borderColor = "#3B82F6";
                  (e.target as HTMLElement).style.background = "#EFF6FF";
                }}
                onMouseLeave={(e) => {
                  (e.target as HTMLElement).style.borderColor = "#E5E7EB";
                  (e.target as HTMLElement).style.background = "white";
                }}
              >
                {option}
              </button>
            ))}
          </div>
        )}

        {/* Free text response */}
        <div style={{ display: "flex", gap: 8 }}>
          <input
            type="text"
            value={customResponse}
            onChange={(e) => setCustomResponse(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleRespond(customResponse)}
            placeholder={hasOptions ? "Or type a custom response..." : "Type your response..."}
            disabled={loading}
            style={{
              flex: 1,
              padding: "10px 14px",
              borderRadius: 8,
              border: "1px solid #E5E7EB",
              fontSize: 14,
              color: "#374151",
              outline: "none",
              background: loading ? "#F9FAFB" : "white",
            }}
          />
          <button
            onClick={() => handleRespond(customResponse)}
            disabled={loading || !customResponse.trim()}
            style={{
              padding: "10px 18px",
              borderRadius: 8,
              border: "none",
              background: loading || !customResponse.trim() ? "#E5E7EB" : "#3B82F6",
              color: loading || !customResponse.trim() ? "#9CA3AF" : "white",
              cursor: loading || !customResponse.trim() ? "not-allowed" : "pointer",
              fontSize: 14,
              fontWeight: 500,
              transition: "all 0.15s ease",
            }}
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </div>

        {error && (
          <p style={{ margin: "8px 0 0", fontSize: 13, color: "#DC2626" }}>
            {error}
          </p>
        )}
      </div>
    </div>
  );
}
