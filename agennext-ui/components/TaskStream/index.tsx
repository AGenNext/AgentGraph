// components/TaskStream/index.tsx
"use client";

import { useTaskStream } from "@/hooks/useTaskStream";
import type { TaskStreamEvent, TaskState } from "@/types/a2a";

interface TaskStreamProps {
  taskId: string;
  mode?: "business" | "developer";
}

const STATE_LABELS: Record<TaskState, string> = {
  submitted: "Submitted",
  working: "Working",
  "input-required": "Waiting for your input",
  completed: "Completed",
  failed: "Failed",
  canceled: "Canceled",
};

const STATE_COLORS: Record<TaskState, string> = {
  submitted: "#6B7280",
  working: "#3B82F6",
  "input-required": "#F59E0B",
  completed: "#10B981",
  failed: "#EF4444",
  canceled: "#6B7280",
};

function BusinessView({ events, state, statusMessage, isDone, isError, errorMessage }: ReturnType<typeof useTaskStream>) {
  const textEvents = events.filter(
    (e) => e.type === "status" && e.status?.message
  );

  return (
    <div style={{ fontFamily: "'DM Sans', sans-serif" }}>
      {/* Status badge */}
      {state && (
        <div style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
          padding: "6px 14px",
          borderRadius: 999,
          background: `${STATE_COLORS[state]}18`,
          border: `1px solid ${STATE_COLORS[state]}40`,
          marginBottom: 20,
        }}>
          {state === "working" && (
            <span style={{
              width: 8, height: 8, borderRadius: "50%",
              background: STATE_COLORS[state],
              animation: "pulse 1.5s infinite",
            }} />
          )}
          <span style={{ color: STATE_COLORS[state], fontSize: 13, fontWeight: 500 }}>
            {STATE_LABELS[state]}
          </span>
        </div>
      )}

      {/* Progress steps */}
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {textEvents.map((event, i) => {
          const text = event.status?.message?.parts
            .filter((p) => p.type === "text")
            .map((p) => (p as { type: "text"; text: string }).text)
            .join("") ?? "";

          const isLast = i === textEvents.length - 1;

          return (
            <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <div style={{
                  width: 24, height: 24, borderRadius: "50%",
                  background: isLast && !isDone ? "#3B82F6" : "#10B981",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  flexShrink: 0,
                }}>
                  {isLast && !isDone ? (
                    <span style={{ width: 8, height: 8, borderRadius: "50%", background: "white" }} />
                  ) : (
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path d="M2 6l3 3 5-5" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  )}
                </div>
                {i < textEvents.length - 1 && (
                  <div style={{ width: 1, height: 20, background: "#E5E7EB", margin: "4px 0" }} />
                )}
              </div>
              <p style={{ margin: 0, fontSize: 14, color: "#374151", lineHeight: 1.5, paddingTop: 2 }}>
                {text}
              </p>
            </div>
          );
        })}

        {/* Loading shimmer when working */}
        {state === "working" && (
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <div style={{
              width: 24, height: 24, borderRadius: "50%",
              background: "#E5E7EB",
              animation: "shimmer 1.5s infinite",
            }} />
            <div style={{
              height: 14, width: 180, borderRadius: 4,
              background: "linear-gradient(90deg, #E5E7EB 25%, #F3F4F6 50%, #E5E7EB 75%)",
              backgroundSize: "200% 100%",
              animation: "shimmer 1.5s infinite",
            }} />
          </div>
        )}
      </div>

      {isError && (
        <div style={{
          marginTop: 16, padding: "12px 16px",
          background: "#FEF2F2", border: "1px solid #FECACA",
          borderRadius: 8, color: "#DC2626", fontSize: 14,
        }}>
          {errorMessage}
        </div>
      )}

      <style>{`
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
        @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
      `}</style>
    </div>
  );
}

function DeveloperView({ events }: ReturnType<typeof useTaskStream>) {
  return (
    <div style={{
      fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
      fontSize: 12,
      background: "#0F172A",
      borderRadius: 8,
      padding: 16,
      maxHeight: 400,
      overflowY: "auto",
    }}>
      {events.length === 0 && (
        <span style={{ color: "#64748B" }}>Waiting for events...</span>
      )}
      {events.map((event, i) => (
        <div key={i} style={{ marginBottom: 8 }}>
          <span style={{ color: "#64748B" }}>{new Date().toISOString()} </span>
          <span style={{
            color: event.type === "error" ? "#F87171"
              : event.type === "artifact" ? "#A78BFA"
              : "#34D399"
          }}>
            [{event.type.toUpperCase()}]
          </span>
          <pre style={{
            margin: "4px 0 0 0",
            color: "#E2E8F0",
            whiteSpace: "pre-wrap",
            wordBreak: "break-all",
          }}>
            {JSON.stringify(event, null, 2)}
          </pre>
        </div>
      ))}
    </div>
  );
}

export function TaskStream({ taskId, mode = "business" }: TaskStreamProps) {
  const streamState = useTaskStream(taskId);

  if (mode === "developer") {
    return <DeveloperView {...streamState} />;
  }

  return <BusinessView {...streamState} />;
}
