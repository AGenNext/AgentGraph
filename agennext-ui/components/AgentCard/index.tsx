// components/AgentCard/index.tsx
"use client";

import type { AgentCardExtended } from "@/types/a2a";

const FRAMEWORK_COLORS: Record<string, { bg: string; text: string; label: string }> = {
  openai:      { bg: "#10A37F18", text: "#10A37F", label: "OpenAI" },
  crewai:      { bg: "#FF6B6B18", text: "#FF6B6B", label: "CrewAI" },
  "google-adk":{ bg: "#4285F418", text: "#4285F4", label: "Google ADK" },
  langgraph:   { bg: "#7C3AED18", text: "#7C3AED", label: "LangGraph" },
  bedrock:     { bg: "#FF980018", text: "#FF9800", label: "AWS Bedrock" },
  anthropic:   { bg: "#CC785C18", text: "#CC785C", label: "Anthropic" },
  salesforce:  { bg: "#00A1E018", text: "#00A1E0", label: "Salesforce" },
  custom:      { bg: "#6B728018", text: "#6B7280", label: "Custom" },
};

function formatDuration(ms?: number): string {
  if (!ms) return "Unknown";
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${(ms / 60000).toFixed(1)}m`;
}

interface AgentCardProps {
  agent: AgentCardExtended;
  variant?: "simple" | "detailed";
  selected?: boolean;
  onSelect?: (agent: AgentCardExtended) => void;
}

export function AgentCard({
  agent,
  variant = "simple",
  selected = false,
  onSelect,
}: AgentCardProps) {
  const framework = agent.framework ?? "custom";
  const fw = FRAMEWORK_COLORS[framework] ?? FRAMEWORK_COLORS.custom;

  if (variant === "simple") {
    return (
      <button
        onClick={() => onSelect?.(agent)}
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 8,
          padding: "16px 18px",
          borderRadius: 12,
          border: selected ? "2px solid #3B82F6" : "1px solid #E5E7EB",
          background: selected ? "#EFF6FF" : "white",
          cursor: onSelect ? "pointer" : "default",
          textAlign: "left",
          width: "100%",
          transition: "all 0.15s ease",
          boxShadow: selected ? "0 0 0 3px #BFDBFE" : "none",
        }}
      >
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <span style={{ fontWeight: 600, fontSize: 15, color: "#111827" }}>
            {agent.name}
          </span>
          <span style={{
            padding: "2px 8px", borderRadius: 999, fontSize: 11, fontWeight: 500,
            background: fw.bg, color: fw.text,
          }}>
            {fw.label}
          </span>
        </div>

        {/* Description */}
        <p style={{ margin: 0, fontSize: 13, color: "#6B7280", lineHeight: 1.5 }}>
          {agent.description}
        </p>

        {/* Meta */}
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {agent.avgCompletionMs && (
            <span style={{ fontSize: 12, color: "#9CA3AF" }}>
              ⏱ ~{formatDuration(agent.avgCompletionMs)}
            </span>
          )}
          {agent.requiresApproval && (
            <span style={{ fontSize: 12, color: "#F59E0B" }}>
              ✋ Requires approval
            </span>
          )}
          {agent.capabilities?.streaming && (
            <span style={{ fontSize: 12, color: "#10B981" }}>
              ⚡ Streaming
            </span>
          )}
        </div>

        {/* Skills */}
        {agent.skills && agent.skills.length > 0 && (
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
            {agent.skills.slice(0, 3).map((skill) => (
              <span key={skill.id} style={{
                padding: "2px 8px", borderRadius: 999,
                background: "#F3F4F6", color: "#374151",
                fontSize: 11, fontWeight: 500,
              }}>
                {skill.name}
              </span>
            ))}
            {agent.skills.length > 3 && (
              <span style={{ fontSize: 11, color: "#9CA3AF", padding: "2px 0" }}>
                +{agent.skills.length - 3} more
              </span>
            )}
          </div>
        )}
      </button>
    );
  }

  // Detailed variant (developer mode)
  return (
    <div style={{
      borderRadius: 12,
      border: "1px solid #E5E7EB",
      background: "white",
      overflow: "hidden",
    }}>
      {/* Header */}
      <div style={{
        padding: "16px 20px",
        borderBottom: "1px solid #F3F4F6",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}>
        <div>
          <h3 style={{ margin: 0, fontSize: 16, fontWeight: 600, color: "#111827" }}>
            {agent.name}
          </h3>
          <a
            href={agent.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{ fontSize: 12, color: "#6B7280", textDecoration: "none" }}
          >
            {agent.url}
          </a>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <span style={{
            padding: "2px 8px", borderRadius: 999, fontSize: 11, fontWeight: 500,
            background: fw.bg, color: fw.text,
          }}>
            {fw.label}
          </span>
          <span style={{
            padding: "2px 8px", borderRadius: 999, fontSize: 11,
            background: "#F3F4F6", color: "#374151",
          }}>
            v{agent.version}
          </span>
        </div>
      </div>

      {/* Skills */}
      <div style={{ padding: "16px 20px" }}>
        <p style={{ margin: "0 0 12px", fontSize: 12, fontWeight: 600, color: "#6B7280", textTransform: "uppercase", letterSpacing: "0.05em" }}>
          Skills
        </p>
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {agent.skills?.map((skill) => (
            <div key={skill.id} style={{
              padding: "10px 14px",
              background: "#F9FAFB",
              borderRadius: 8,
            }}>
              <div style={{ fontWeight: 500, fontSize: 13, color: "#111827" }}>{skill.name}</div>
              <div style={{ fontSize: 12, color: "#6B7280", marginTop: 2 }}>{skill.description}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Capabilities */}
      <div style={{ padding: "0 20px 16px" }}>
        <p style={{ margin: "0 0 8px", fontSize: 12, fontWeight: 600, color: "#6B7280", textTransform: "uppercase", letterSpacing: "0.05em" }}>
          Capabilities
        </p>
        <div style={{ display: "flex", gap: 8 }}>
          {agent.capabilities && Object.entries(agent.capabilities).map(([key, val]) => val && (
            <span key={key} style={{
              padding: "3px 10px", borderRadius: 999, fontSize: 11,
              background: "#ECFDF5", color: "#059669",
            }}>
              {key}
            </span>
          ))}
        </div>
      </div>

      {/* Raw JSON toggle */}
      <details style={{ borderTop: "1px solid #F3F4F6" }}>
        <summary style={{
          padding: "10px 20px", fontSize: 12, color: "#6B7280",
          cursor: "pointer", userSelect: "none",
        }}>
          Raw AgentCard JSON
        </summary>
        <pre style={{
          margin: 0, padding: "12px 20px",
          background: "#0F172A", color: "#E2E8F0",
          fontSize: 11, overflowX: "auto",
        }}>
          {JSON.stringify(agent, null, 2)}
        </pre>
      </details>
    </div>
  );
}
