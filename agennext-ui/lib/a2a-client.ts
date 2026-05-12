// lib/a2a-client.ts
// Talks to your AGenNext Python backend + external A2A agents
// Built on top of @a2a-js/sdk client

import {
  // SDK Client
  A2AClient,
  Client,
} from "@a2a-js/sdk/client";

import type {
  // Types from main SDK
  MessageSendParams,
  SendMessageResponse,
  Task,
  TaskQueryParams,
  TaskIdParams,
  CancelTaskResponse,
  GetTaskResponse,
  PushNotificationConfig,
  GetTaskPushNotificationConfigParams,
  SetTaskPushNotificationConfigResponse,
  ListTaskPushNotificationConfigParams,
  DeleteTaskPushNotificationConfigParams,
  AgentCard,
} from "@a2a-js/sdk";

import type {
  AgentCardExtended,
  TaskSubmission,
  ApprovalRequest,
  TaskStreamEvent,
} from "@/types/a2a";

// Re-export SDK types
export type {
  AgentCard,
  MessageSendParams,
  SendMessageResponse,
  Task,
  TaskQueryParams,
  TaskIdParams,
  CancelTaskResponse,
  GetTaskResponse,
  PushNotificationConfig,
  GetTaskPushNotificationConfigParams,
  SetTaskPushNotificationConfigResponse,
  ListTaskPushNotificationConfigParams,
  DeleteTaskPushNotificationConfigParams,
} from "@a2a-js/sdk";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

// ─── AGenNext Backend Client (Legacy) ────────────────────────────────────────

export async function listBackendAgents(): Promise<AgentCardExtended[]> {
  const res = await fetch(`${BACKEND_URL}/agents`, {
    next: { revalidate: 30 },
  });
  if (!res.ok) throw new Error(`Failed to fetch agents: ${res.statusText}`);
  return res.json();
}

export async function getAgentCard(agentUrl: string): Promise<AgentCardExtended> {
  // Fetch AgentCard from /.well-known/agent.json on the agent's server
  const wellKnownUrl = `${agentUrl.replace(/\/$/, "")}/.well-known/agent.json`;
  const res = await fetch(wellKnownUrl);
  if (!res.ok) throw new Error(`Failed to fetch agent card from ${wellKnownUrl}`);
  return res.json();
}

export async function registerAgent(agentUrl: string): Promise<AgentCardExtended> {
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

// Legacy: Get task from backend
export async function getBackendTask(taskId: string): Promise<Task> {
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

// Legacy: Cancel task in backend
export async function cancelBackendTask(taskId: string): Promise<void> {
  const res = await fetch(`${BACKEND_URL}/tasks/${taskId}/cancel`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Failed to cancel task: ${res.statusText}`);
}

// ─── Approval Enforcement ────────────────────────────────────────────────────────────

/**
 * Task context requirements for pre-flight verification
 */
export interface TaskContext {
  /** What needs to be done */
  goal: string;
  /** Required credentials (API keys, tokens, etc.) */
  credentials?: Record<string, string>;
  /** Repository details */
  repo?: {
    url: string;
    branch?: string;
    path?: string;
  };
  /** Import/export specifications */
  imports?: string[];
  exports?: string[];
  /** UI/UX clarifications */
  uiClarifications?: {
    theme?: string;
    responsive?: boolean;
    accessibility?: string[];
  };
  /** Any other context needed */
  details?: Record<string, unknown>;
}

/**
 * Submit task with FULL context required before execution
 * Agent must gather all info BEFORE starting work
 */
export async function submitWithPreFlight(
  submission: TaskSubmission
): Promise<{ taskId: string; status: "pending-context"; requiredFields: string[] }> {
  const res = await fetch(`${BACKEND_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...submission,
      // Force pre-flight check mode
      preFlightRequired: true,
      // Require these fields before execution
      requiredContext: [
        "credentials",    // Must ask for any API keys/tokens
        "repoDetails",  // Must clarify repo URL, branch
        "importsExports", // Must clarify dependencies
        "uiClarifications", // Must clarify UI requirements
      ],
    }),
  });
  if (!res.ok) throw new Error(`Failed to submit task: ${res.statusText}`);
  return res.json();
}

/**
 * Submit and BLOCK until ALL context is gathered
 * Agent asks questions, human answers, then agent proceeds
 */
export async function submitAndGatherContext(
  submission: TaskSubmission,
  context: TaskContext,
  onClarificationNeeded?: (question: string, options?: string[]) => void
): Promise<Task> {
  // Submit with pre-flight
  const { taskId } = await submitWithPreFlight(submission);

  // First, ask for any missing context
  const missingFields: string[] = [];

  if (!context.credentials) {
    missingFields.push("credentials");
    onClarificationNeeded?.("What credentials are needed for this task?", [
      "GitHub token",
      "npm/pip keys",
      "API keys",
      "None required",
    ]);
  }

  if (!context.repo) {
    missingFields.push("repoDetails");
    onClarificationNeeded?.("Which repository should I use?", [
      "Current repo",
      "External repo URL",
    ]);
  }

  if (!context.imports) {
    missingFields.push("importsExports");
    onClarificationNeeded?.("Any specific imports needed?", [
      "From SDK",
      "From npm",
      "Custom only",
    ]);
  }

  if (!context.uiClarifications) {
    missingFields.push("uiClarifications");
    onClarificationNeeded?.("Any UI requirements?", [
      "Theme/preferences",
      "Responsive behavior",
      "Accessibility needs",
    ]);
  }

  // If we have context, submit it to complete pre-flight
  if (context.credentials || context.repo || context.imports || context.uiClarifications) {
    await provideTaskContext(taskId, context);
  }

  // Poll for approval after context is provided
  return pollForApproval(taskId);
}

/**
 * Provide missing context to a pending task
 */
export async function provideTaskContext(
  taskId: string,
  context: TaskContext
): Promise<void> {
  const res = await fetch(`${BACKEND_URL}/tasks/${taskId}/context`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(context),
  });
  if (!res.ok) throw new Error(`Failed to provide context: ${res.statusText}`);
}

// ─── Checkpoint System ─────────────────────────────────────────────────────────────
// At each checkpoint: save context, memory, knowledgebase, learnings


/** What gets saved at each checkpoint */
export interface CheckpointState {
  /** Step number */
  step: number;
  /** What the agent learned so far */
  learnings: string[];
  /** Key decisions made */
  decisions: { reason: string; outcome: string }[];
  /** Errors/mistakes and how they were fixed */
  mistakesFixed: { error: string; fix: string }[];
  /** Current context state */
  context: TaskContext;
  /** Files modified so far */
  filesModified: string[];
  /** Any new knowledge to remember */
  knowledgeBase: Record<string, unknown>;
  /** Timestamp */
  savedAt: string;
}

/**
 * A checkpoint where agent pauses, saves state, then continues
 */
export interface CheckpointConfig {
  id: string;
  description: string;
  /** Scope: repo, file, function, api, deploy */
  scope: "repo" | "file" | "function" | "api" | "deploy";
}

/**
 * Submit task with CHECKPOINTS
 * - Agent stops at each checkpoint to SAVE STATE
 * - Then continues (resume from checkpoint if stopped)
 */
export async function submitWithCheckpoints(
  submission: TaskSubmission,
  checkpoints: CheckpointConfig[]
): Promise<{ taskId: string; checkpoints: CheckpointConfig[] }> {
  const res = await fetch(`${BACKEND_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...submission,
      // Enable checkpoints
      useCheckpoints: true,
      checkpoints: checkpoints,
      // Save full state at each checkpoint
      saveStateAtEachCheckpoint: true,
    }),
  });
  if (!res.ok) throw new Error(`Failed to submit: ${res.statusText}`);
  return res.json();
}

/**
 * Get current checkpoint state (what was saved)
 */
export async function getCheckpointState(
  taskId: string
): Promise<CheckpointState> {
  const res = await fetch(`${BACKEND_URL}/tasks/${taskId}/checkpoint/state`);
  if (!res.ok) throw new Error(`Failed to get state: ${res.statusText}`);
  return res.json();
}

/**
 * Get all past checkpoints for a task
 */
export async function getCheckpointHistory(
  taskId: string
): Promise<CheckpointState[]> {
  const res = await fetch(`${BACKEND_URL}/tasks/${taskId}/checkpoint/history`);
  if (!res.ok) throw new Error(`Failed to get history: ${res.statusText}`);
  return res.json();
}

/**
 * Resume task from a specific checkpoint
 * Picks up from saved state, preserving learnings
 */
export async function resumeFromCheckpoint(
  taskId: string,
  checkpointIndex?: number
): Promise<{ taskId: string; resumedFrom: number }> {
  const idx = checkpointIndex ?? -1; // Default to last checkpoint
  
  const res = await fetch(`${BACKEND_URL}/tasks/${taskId}/checkpoint/${idx}/resume`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Failed to resume: ${res.statusText}`);
  return res.json();
}

/**
 * Get all learnings accumulated across all runs
 */
export async function getAllLearnings(
  taskId: string
): Promise<{
  totalMistakesFixed: number;
  learnings: string[];
  knowledgeBase: Record<string, unknown>;
}> {
  const res = await fetch(`${BACKEND_URL}/tasks/${taskId}/learnings`);
  if (!res.ok) throw new Error(`Failed to get learnings: ${res.statusText}`);
  return res.json();
}

/**
 * Submit a task that REQUIRES approval before execution
 * Use this to force human-in-the-loop for sensitive operations
 */
export async function submitWithApproval(
  submission: TaskSubmission
): Promise<{ taskId: string; requiresApproval: true }> {
  const res = await fetch(`${BACKEND_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...submission,
      // Force approval required flag
      approvalRequired: true,
      // Block until approved
      waitForApproval: true,
    }),
  });
  if (!res.ok) throw new Error(`Failed to submit task: ${res.statusText}`);
  return res.json();
}

/**
 * Submit a task and wait until explicitly approved
 * Blocks until human responds to approval request
 */
export async function submitAndWaitForApproval(
  submission: TaskSubmission,
  onApprovalRequired?: (taskId: string) => void
): Promise<Task> {
  // First submit with approval required
  const { taskId } = await submitWithApproval(submission);

  // Notify callback if provided
  onApprovalRequired?.(taskId);

  // Poll for completion once approved
  return pollForApproval(taskId);
}

/**
 * Poll a task until approved or rejected
 */
async function pollForApproval(taskId: string, interval = 2000): Promise<Task> {
  while (true) {
    const res = await fetch(`${BACKEND_URL}/tasks/${taskId}`);

    if (!res.ok) throw new Error(`Failed to fetch task: ${res.statusText}`);

    const task = await res.json();

    // Check if approved (task can proceed)
    if (task.status === "approved" || task.status === "running" || task.status === "completed") {
      return task;
    }

    // Check if rejected
    if (task.status === "rejected" || task.status === "failed") {
      throw new Error(`Task ${task.status}: ${task.error}`);
    }

    // Still pending approval
    await new Promise((r) => setTimeout(r, interval));
  }
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

// Backward compatibility: wrap async function for direct calling
export async function listAgents(): Promise<AgentCardExtended[]> {
  return listBackendAgents();
}

// ─── SDK Client Export ───────────────────────────────────────────────────────
// Use these for A2A-compliant agents instead of legacy backend

export { A2AClient, Client } from "@a2a-js/sdk/client";
