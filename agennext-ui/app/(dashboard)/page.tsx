// app/(dashboard)/page.tsx
"use client";

import { useState, useEffect } from "react";
import { listAgents, submitTask } from "@/lib/a2a-client";
import { AgentCard } from "@/components/AgentCard";
import { TaskStream } from "@/components/TaskStream";
import type { AgentCardExtended, Task } from "@/types/a2a";

export default function DashboardPage() {
  const [agents, setAgents] = useState<AgentCardExtended[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<AgentCardExtended | null>(null);
  const [message, setMessage] = useState("");
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [agentsLoading, setAgentsLoading] = useState(true);

  useEffect(() => {
    listAgents()
      .then(setAgents)
      .catch(() => setError("Failed to load agents"))
      .finally(() => setAgentsLoading(false));
  }, []);

  const handleSubmit = async () => {
    if (!selectedAgent || !selectedAgent.url || !message.trim()) return;
    setLoading(true);
    setError(null);
    setTask(null);
    try {
      const newTask = await submitTask({
        agentUrl: selectedAgent.url,
        message: message.trim(),
      });
      setTask(newTask);
      setMessage("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to submit task");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "#F9FAFB",
      fontFamily: "'DM Sans', -apple-system, sans-serif",
    }}>
      {/* Top nav */}
      <nav style={{
        background: "white",
        borderBottom: "1px solid #E5E7EB",
        padding: "0 32px",
        height: 56,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 28, height: 28, borderRadius: 7,
            background: "linear-gradient(135deg, #3B82F6, #7C3AED)",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <span style={{ fontSize: 14 }}>⚡</span>
          </div>
          <span style={{ fontWeight: 700, fontSize: 16, color: "#111827" }}>AGenNext</span>
        </div>
        <a href="/workspace" style={{
          fontSize: 13, color: "#6B7280", textDecoration: "none",
          padding: "5px 12px", borderRadius: 6, border: "1px solid #E5E7EB",
        }}>
          Developer mode →
        </a>
      </nav>

      <div style={{ maxWidth: 900, margin: "0 auto", padding: "40px 24px" }}>
        <h1 style={{ margin: "0 0 4px", fontSize: 26, fontWeight: 700, color: "#111827" }}>
          Run a task
        </h1>
        <p style={{ margin: "0 0 32px", color: "#6B7280", fontSize: 15 }}>
          Pick an agent and describe what you need done.
        </p>

        {/* Agent picker */}
        <section style={{ marginBottom: 28 }}>
          <h2 style={{ margin: "0 0 14px", fontSize: 14, fontWeight: 600, color: "#374151", textTransform: "uppercase", letterSpacing: "0.05em" }}>
            1. Choose an agent
          </h2>

          {agentsLoading ? (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 12 }}>
              {[1, 2, 3].map((i) => (
                <div key={i} style={{
                  height: 120, borderRadius: 12, background: "#E5E7EB",
                  animation: "shimmer 1.5s infinite",
                }} />
              ))}
            </div>
          ) : agents.length === 0 ? (
            <div style={{
              padding: "32px", textAlign: "center",
              border: "2px dashed #E5E7EB", borderRadius: 12,
              color: "#9CA3AF", fontSize: 14,
            }}>
              No agents registered yet.{" "}
              <a href="/workspace/agents" style={{ color: "#3B82F6" }}>Register one →</a>
            </div>
          ) : (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 12 }}>
              {agents.map((agent) => (
                <AgentCard
                  key={agent.url}
                  agent={agent}
                  variant="simple"
                  selected={selectedAgent?.url === agent.url}
                  onSelect={setSelectedAgent}
                />
              ))}
            </div>
          )}
        </section>

        {/* Task input */}
        <section style={{ marginBottom: 28 }}>
          <h2 style={{ margin: "0 0 14px", fontSize: 14, fontWeight: 600, color: "#374151", textTransform: "uppercase", letterSpacing: "0.05em" }}>
            2. Describe the task
          </h2>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={
              selectedAgent
                ? `What do you want ${selectedAgent.name} to do?`
                : "Select an agent first..."
            }
            disabled={!selectedAgent || loading}
            rows={4}
            style={{
              width: "100%",
              padding: "14px 16px",
              borderRadius: 10,
              border: "1px solid #E5E7EB",
              fontSize: 15,
              color: "#374151",
              resize: "vertical",
              outline: "none",
              fontFamily: "inherit",
              background: !selectedAgent ? "#F9FAFB" : "white",
              boxSizing: "border-box",
            }}
          />
        </section>

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={!selectedAgent || !message.trim() || loading}
          style={{
            padding: "12px 28px",
            borderRadius: 10,
            border: "none",
            background: !selectedAgent || !message.trim() || loading
              ? "#E5E7EB"
              : "linear-gradient(135deg, #3B82F6, #7C3AED)",
            color: !selectedAgent || !message.trim() || loading ? "#9CA3AF" : "white",
            fontSize: 15,
            fontWeight: 600,
            cursor: !selectedAgent || !message.trim() || loading ? "not-allowed" : "pointer",
            transition: "all 0.15s ease",
          }}
        >
          {loading ? "Submitting..." : "Run task →"}
        </button>

        {error && (
          <p style={{ marginTop: 12, color: "#DC2626", fontSize: 14 }}>{error}</p>
        )}

        {/* Task stream */}
        {task && (
          <section style={{ marginTop: 40 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
              <h2 style={{ margin: 0, fontSize: 14, fontWeight: 600, color: "#374151", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                Task progress
              </h2>
              <span style={{ fontSize: 12, color: "#9CA3AF", fontFamily: "monospace" }}>
                {task.id}
              </span>
            </div>
            <div style={{
              background: "white",
              borderRadius: 12,
              border: "1px solid #E5E7EB",
              padding: "20px 24px",
            }}>
              <TaskStream taskId={task.id} mode="business" />
            </div>
          </section>
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
