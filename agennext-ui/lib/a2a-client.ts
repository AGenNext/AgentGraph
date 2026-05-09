// lib/a2a-client.ts
// Talks to your AGenNext Python backend + external A2A agents

import type {
  AgentCard,
  Task,
  TaskSubmission,
  TaskStreamEvent,
  ApprovalRequest,
} from "@/types/a2a";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

// ─── Agent Registry ──────────────────────────────────────────────────────────

export async function listAgents(): Promise<AgentCard[]> {
  const res = await fetch(`${BACKEND_URL}/agents`, {
    next: { revalidate: 30 },
  });
  if (!res.ok) throw new Error(`Failed to fetch agents: ${res.statusText}`);
  return res.json();
}

export async function getAgentCard(agentUrl: string): Promise<AgentCard> {
  // Fetch AgentCard from /.well-known/agent.json on the agent's server
  const wellKnownUrl = `${agentUrl.replace(/\/$/, "")}/.well-known/agent.json`;
  const res = await fetch(wellKnownUrl);
  if (!res.ok) throw new Error(`Failed to fetch agent card from ${wellKnownUrl}`);
  return res.json();
}

export async function registerAgent(agentUrl: string): Promise<AgentCard> {
  const res = await fetch(`${BACKEND_URL}/agents/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: agentUrl }),
  });
  if (!res.ok) throw new Error(`Failed to register agent: ${res.statusText}`);
  return res.json();
}

// ─── Task Management ─────────────────────────────────────────────────────────

export async function submitTask(submission: TaskSubmission): Promise<Task> {
  const res = await fetch(`${BACKEND_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(submission),
  });
  if (!res.ok) throw new Error(`Failed to submit task: ${res.statusText}`);
  return res.json();
}

export async function getTask(taskId: string): Promise<Task> {
  const res = await fetch(`${BACKEND_URL}/tasks/${taskId}`);
  if (!res.ok) throw new Error(`Failed to fetch task: ${res.statusText}`);
  return res.json();
}

export async function listTasks(params?: {
  state?: string;
  agentUrl?: string;
  limit?: number;
  offset?: number;
}): Promise<{ tasks: Task[]; total: number }> {
  const query = new URLSearchParams();
  if (params?.state) query.set("state", params.state);
  if (params?.agentUrl) query.set("agentUrl", params.agentUrl);
  if (params?.limit) query.set("limit", String(params.limit));
  if (params?.offset) query.set("offset", String(params.offset));

  const res = await fetch(`${BACKEND_URL}/tasks?${query}`);
  if (!res.ok) throw new Error(`Failed to list tasks: ${res.statusText}`);
  return res.json();
}

export async function cancelTask(taskId: string): Promise<void> {
  const res = await fetch(`${BACKEND_URL}/tasks/${taskId}/cancel`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Failed to cancel task: ${res.statusText}`);
}

// ─── SSE Stream ──────────────────────────────────────────────────────────────

export function createTaskStream(
  taskId: string,
  handlers: {
    onEvent: (event: TaskStreamEvent) => void;
    onError?: (err: Event) => void;
    onDone?: () => void;
  }
): () => void {
  const es = new EventSource(`${BACKEND_URL}/tasks/${taskId}/stream`);

  es.onmessage = (e) => {
    try {
      const event: TaskStreamEvent = JSON.parse(e.data);
      handlers.onEvent(event);
      if (event.final) {
        es.close();
        handlers.onDone?.();
      }
    } catch {
      console.error("Failed to parse SSE event", e.data);
    }
  };

  es.onerror = (e) => {
    handlers.onError?.(e);
    es.close();
  };

  // Return cleanup function
  return () => es.close();
}

// ─── Approvals ───────────────────────────────────────────────────────────────

export async function listPendingApprovals(): Promise<ApprovalRequest[]> {
  const res = await fetch(`${BACKEND_URL}/approvals`);
  if (!res.ok) throw new Error(`Failed to fetch approvals: ${res.statusText}`);
  return res.json();
}

export async function respondToApproval(
  taskId: string,
  response: string
): Promise<void> {
  const res = await fetch(`${BACKEND_URL}/approvals/${taskId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ response }),
  });
  if (!res.ok) throw new Error(`Failed to respond to approval: ${res.statusText}`);
}
