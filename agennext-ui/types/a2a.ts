// A2A Protocol Types
// Aligned with a2aproject/A2A spec

export type TaskState =
  | "submitted"
  | "working"
  | "input-required"
  | "completed"
  | "failed"
  | "canceled";

export interface AgentSkill {
  id: string;
  name: string;
  description: string;
  inputModes?: string[];
  outputModes?: string[];
  tags?: string[];
}

export interface AgentCapabilities {
  streaming?: boolean;
  pushNotifications?: boolean;
  stateTransitionHistory?: boolean;
}

export interface AgentCard {
  name: string;
  description: string;
  url: string;
  version: string;
  provider?: {
    organization: string;
    url?: string;
  };
  capabilities: AgentCapabilities;
  skills: AgentSkill[];
  defaultInputModes?: string[];
  defaultOutputModes?: string[];
  // AGenNext extensions
  framework?: "openai" | "crewai" | "google-adk" | "langgraph" | "bedrock" | "anthropic" | "salesforce" | "custom";
  avgCompletionMs?: number;
  requiresApproval?: boolean;
  tags?: string[];
}

export interface TaskMessage {
  role: "user" | "agent";
  parts: MessagePart[];
}

export type MessagePart =
  | { type: "text"; text: string }
  | { type: "file"; file: { mimeType: string; uri?: string; bytes?: string; name?: string } }
  | { type: "data"; data: Record<string, unknown> };

export interface TaskArtifact {
  name?: string;
  description?: string;
  index: number;
  parts: MessagePart[];
  lastChunk?: boolean;
  metadata?: Record<string, unknown>;
}

export interface TaskStatus {
  state: TaskState;
  message?: TaskMessage;
  timestamp: string;
}

export interface Task {
  id: string;
  sessionId?: string;
  status: TaskStatus;
  artifacts?: TaskArtifact[];
  history?: TaskStatus[];
  metadata?: Record<string, unknown>;
  // AGenNext extensions
  agentUrl?: string;
  agentName?: string;
  framework?: AgentCard["framework"];
  createdAt: string;
  updatedAt: string;
  submittedBy?: string;
}

// SSE Event types
export interface TaskStreamEvent {
  id?: string;
  type: "status" | "artifact" | "error";
  taskId: string;
  // for status events
  status?: TaskStatus;
  final?: boolean;
  // for artifact events
  artifact?: TaskArtifact;
  // for error events
  error?: { code: number; message: string };
}

// Approval types
export interface ApprovalRequest {
  taskId: string;
  agentName: string;
  question: string;
  context?: string;
  options?: string[];
  createdAt: string;
  expiresAt?: string;
}

// Task submission
export interface TaskSubmission {
  agentUrl: string;
  message: string;
  sessionId?: string;
  metadata?: Record<string, unknown>;
}
