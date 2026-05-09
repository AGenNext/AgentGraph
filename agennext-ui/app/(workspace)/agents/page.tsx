// app/(workspace)/agents/page.tsx
"use client";

import { useState, useEffect } from "react";
import { listAgents, registerAgent } from "@/lib/a2a-client";
import { AgentCard } from "@/components/AgentCard";
import type { AgentCard as AgentCardType } from "@/types/a2a";

export default function AgentsWorkspacePage() {
  const [agents, setAgents] = useState<AgentCardType[]>([]);
  const [loading, setLoading] = useState(true);
  const [registerUrl, setRegisterUrl] = useState("");
  const [registering, setRegistering] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<AgentCardType | null>(null);

  useEffect(() => {
    listAgents()
      .then(setAgents)
      .finally(() => setLoading(false));
  }, []);

  const handleRegister = async () => {
    if (!registerUrl.trim()) return;
    setRegistering(true);
    setError(null);
    try {
      const card = await registerAgent(registerUrl.trim());
      setAgents((prev) => [...prev, card]);
      setRegisterUrl("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to register agent");
    } finally {
      setRegistering(false);
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0F172A",
      color: "#E2E8F0",
      fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
    }}>
      {/* Nav */}
      <nav style={{
        borderBottom: "1px solid #1E293B",
        padding: "0 32px",
        height: 52,
        display: "flex",
        alignItems: "center",
        gap: 24,
      }}>
        <a href="/" style={{ fontSize: 12, color: "#64748B", textDecoration: "none" }}>← Dashboard</a>
        <span style={{ fontSize: 13, color: "#94A3B8" }}>Developer Workspace</span>
        <span style={{ fontSize: 12, color: "#3B82F6" }}>/ Agents</span>
      </nav>

      <div style={{ maxWidth: 1000, margin: "0 auto", padding: "32px 24px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 28 }}>
          <div>
            <h1 style={{ margin: "0 0 4px", fontSize: 20, fontWeight: 600, color: "#F1F5F9" }}>
              Agent Registry
            </h1>
            <p style={{ margin: 0, fontSize: 13, color: "#64748B" }}>
              {agents.length} registered agent{agents.length !== 1 ? "s" : ""}
            </p>
          </div>

          {/* Register new agent */}
          <div style={{ display: "flex", gap: 8 }}>
            <input
              type="text"
              value={registerUrl}
              onChange={(e) => setRegisterUrl(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleRegister()}
              placeholder="https://agent.example.com"
              style={{
                padding: "8px 14px",
                borderRadius: 7,
                border: "1px solid #1E293B",
                background: "#1E293B",
                color: "#E2E8F0",
                fontSize: 12,
                width: 260,
                outline: "none",
              }}
            />
            <button
              onClick={handleRegister}
              disabled={registering || !registerUrl.trim()}
              style={{
                padding: "8px 16px",
                borderRadius: 7,
                border: "none",
                background: registering || !registerUrl.trim() ? "#1E293B" : "#3B82F6",
                color: registering || !registerUrl.trim() ? "#475569" : "white",
                cursor: registering || !registerUrl.trim() ? "not-allowed" : "pointer",
                fontSize: 12,
                fontWeight: 500,
              }}
            >
              {registering ? "Registering..." : "+ Register"}
            </button>
          </div>
        </div>

        {error && (
          <div style={{
            marginBottom: 16, padding: "10px 14px",
            background: "#450A0A", border: "1px solid #7F1D1D",
            borderRadius: 7, color: "#FCA5A5", fontSize: 12,
          }}>
            {error}
          </div>
        )}

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          {/* Agent list */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {loading ? (
              [1, 2, 3].map((i) => (
                <div key={i} style={{
                  height: 80, borderRadius: 8, background: "#1E293B",
                  animation: "shimmer 1.5s infinite",
                }} />
              ))
            ) : agents.length === 0 ? (
              <div style={{
                padding: "32px", textAlign: "center",
                border: "1px dashed #1E293B", borderRadius: 8,
                color: "#475569", fontSize: 12,
              }}>
                No agents registered. Add one above.
              </div>
            ) : (
              agents.map((agent) => (
                <button
                  key={agent.url}
                  onClick={() => setSelected(agent)}
                  style={{
                    padding: "12px 16px",
                    borderRadius: 8,
                    border: selected?.url === agent.url ? "1px solid #3B82F6" : "1px solid #1E293B",
                    background: selected?.url === agent.url ? "#172554" : "#1E293B",
                    cursor: "pointer",
                    textAlign: "left",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <div>
                    <div style={{ fontSize: 13, color: "#F1F5F9", fontWeight: 500 }}>{agent.name}</div>
                    <div style={{ fontSize: 11, color: "#64748B", marginTop: 2 }}>{agent.url}</div>
                  </div>
                  <span style={{
                    fontSize: 10, padding: "2px 7px", borderRadius: 999,
                    background: "#0F172A", color: "#94A3B8",
                  }}>
                    {agent.framework ?? "custom"}
                  </span>
                </button>
              ))
            )}
          </div>

          {/* Detail panel */}
          <div>
            {selected ? (
              <AgentCard agent={selected} variant="detailed" />
            ) : (
              <div style={{
                height: "100%", minHeight: 200,
                border: "1px dashed #1E293B", borderRadius: 8,
                display: "flex", alignItems: "center", justifyContent: "center",
                color: "#475569", fontSize: 12,
              }}>
                Select an agent to inspect
              </div>
            )}
          </div>
        </div>
      </div>

      <style>{`
        @keyframes shimmer {
          0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}
