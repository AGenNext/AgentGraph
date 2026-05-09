// Re-export ALL types from official @a2a-js SDK
import type {
  // Error types
  A2AError,
  JSONParseError,
  InvalidRequestError,
  MethodNotFoundError,
  InvalidParamsError,
  InternalError,
  TaskNotFoundError,
  TaskNotCancelableError,
  PushNotificationNotSupportedError,
  UnsupportedOperationError,
  ContentTypeNotSupportedError,
  InvalidAgentResponseError,
  AuthenticatedExtendedCardNotConfiguredError,
  // Request types
  SendMessageRequest,
  SendStreamingMessageRequest,
  GetTaskRequest,
  CancelTaskRequest,
  SetTaskPushNotificationConfigRequest,
  GetTaskPushNotificationConfigRequest,
  ListTaskPushNotificationConfigRequest,
  DeleteTaskPushNotificationConfigRequest,
  GetAuthenticatedExtendedCardRequest,
  TaskResubscriptionRequest,
  // Response types
  SendMessageSuccessResponse,
  SendStreamingMessageSuccessResponse,
  GetTaskSuccessResponse,
  CancelTaskSuccessResponse,
  SetTaskPushNotificationConfigSuccessResponse,
  GetTaskPushNotificationConfigSuccessResponse,
  ListTaskPushNotificationConfigSuccessResponse,
  DeleteTaskPushNotificationConfigSuccessResponse,
  GetAuthenticatedExtendedCardSuccessResponse,
  JSONRPCErrorResponse,
  // Param types
  MessageSendParams,
  MessageSendParams1,
  MessageSendConfiguration,
  MessageSendConfiguration1,
  TaskQueryParams,
  TaskIdParams,
  TaskIdParams1,
  TaskIdParams2,
  GetTaskPushNotificationConfigParams,
  ListTaskPushNotificationConfigParams,
  DeleteTaskPushNotificationConfigParams,
  // Push notification types
  PushNotificationConfig,
  PushNotificationConfig1,
  PushNotificationAuthenticationInfo,
  // Agent types
  AgentCard,
  AgentCard1,
  AgentSkill,
  AgentCapabilities,
  AgentCapabilities1,
  AgentProvider,
  AgentProvider1,
  AgentExtension,
  AgentInterface,
  AgentCardSignature,
  // Task types
  Task,
  Task1,
  Task2,
  TaskState,
  TaskStatus,
  TaskStatus1,
  TaskStatus2,
  TaskStatusUpdateEvent,
  TaskArtifactUpdateEvent,
  // Message types
  Message,
  Message1,
  Message2,
  TextPart,
  FilePart,
  FileWithBytes,
  FileWithUri,
  DataPart,
  Part,
  PartBase,
  Artifact,
  Artifact1,
  // OAuth/Security types
  OAuthFlows,
  OAuthFlows1,
  AuthorizationCodeOAuthFlow,
  AuthorizationCodeOAuthFlow1,
  ClientCredentialsOAuthFlow,
  ClientCredentialsOAuthFlow1,
  ImplicitOAuthFlow,
  ImplicitOAuthFlow1,
  PasswordOAuthFlow,
  PasswordOAuthFlow1,
  APIKeySecurityScheme,
  HTTPAuthSecurityScheme,
  OAuth2SecurityScheme,
  OpenIdConnectSecurityScheme,
  MutualTLSSecurityScheme,
  SecurityScheme,
  SecuritySchemeBase,
  // Utility types
  TransportProtocol,
  Extensions,
  ExtensionURI,
  MySchema,
  JSONRPCMessage,
  JSONRPCRequest,
  JSONRPCResponse,
  JSONRPCSuccessResponse,
  JSONRPCError,
  // Aggregate response types
  A2AResponse,
  SendMessageResponse,
  SendStreamingMessageResponse,
  GetTaskResponse,
  CancelTaskResponse,
  GetTaskPushNotificationConfigResponse,
  SetTaskPushNotificationConfigResponse,
  DeleteTaskPushNotificationConfigResponse,
  ListTaskPushNotificationConfigResponse,
  GetAuthenticatedExtendedCardResponse,
} from "@a2a-js/sdk";

// Re-export all types for consumers
export type {
  // Errors
  A2AError,
  JSONParseError,
  InvalidRequestError,
  MethodNotFoundError,
  InvalidParamsError,
  InternalError,
  TaskNotFoundError,
  TaskNotCancelableError,
  PushNotificationNotSupportedError,
  UnsupportedOperationError,
  ContentTypeNotSupportedError,
  InvalidAgentResponseError,
  AuthenticatedExtendedCardNotConfiguredError,
  // Requests
  SendMessageRequest,
  SendStreamingMessageRequest,
  GetTaskRequest,
  CancelTaskRequest,
  SetTaskPushNotificationConfigRequest,
  GetTaskPushNotificationConfigRequest,
  ListTaskPushNotificationConfigRequest,
  DeleteTaskPushNotificationConfigRequest,
  GetAuthenticatedExtendedCardRequest,
  TaskResubscriptionRequest,
  // Responses
  SendMessageSuccessResponse,
  SendStreamingMessageSuccessResponse,
  GetTaskSuccessResponse,
  CancelTaskSuccessResponse,
  SetTaskPushNotificationConfigSuccessResponse,
  GetTaskPushNotificationConfigSuccessResponse,
  ListTaskPushNotificationConfigSuccessResponse,
  DeleteTaskPushNotificationConfigSuccessResponse,
  GetAuthenticatedExtendedCardSuccessResponse,
  JSONRPCErrorResponse,
  // Params
  MessageSendParams,
  MessageSendParams1,
  MessageSendConfiguration,
  MessageSendConfiguration1,
  TaskQueryParams,
  TaskIdParams,
  TaskIdParams1,
  TaskIdParams2,
  GetTaskPushNotificationConfigParams,
  ListTaskPushNotificationConfigParams,
  DeleteTaskPushNotificationConfigParams,
  // Push notifications
  PushNotificationConfig,
  PushNotificationConfig1,
  PushNotificationAuthenticationInfo,
  // Agents
  AgentCard,
  AgentCard1,
  AgentSkill,
  AgentCapabilities,
  AgentCapabilities1,
  AgentProvider,
  AgentProvider1,
  AgentExtension,
  AgentInterface,
  AgentCardSignature,
  // Tasks
  Task,
  Task1,
  Task2,
  TaskState,
  TaskStatus,
  TaskStatus1,
  TaskStatus2,
  TaskStatusUpdateEvent,
  TaskArtifactUpdateEvent,
  // Messages
  Message,
  Message1,
  Message2,
  TextPart,
  FilePart,
  FileWithBytes,
  FileWithUri,
  DataPart,
  Part,
  PartBase,
  Artifact,
  Artifact1,
  // OAuth/Security
  OAuthFlows,
  OAuthFlows1,
  AuthorizationCodeOAuthFlow,
  AuthorizationCodeOAuthFlow1,
  ClientCredentialsOAuthFlow,
  ClientCredentialsOAuthFlow1,
  ImplicitOAuthFlow,
  ImplicitOAuthFlow1,
  PasswordOAuthFlow,
  PasswordOAuthFlow1,
  APIKeySecurityScheme,
  HTTPAuthSecurityScheme,
  OAuth2SecurityScheme,
  OpenIdConnectSecurityScheme,
  MutualTLSSecurityScheme,
  SecurityScheme,
  SecuritySchemeBase,
  // Utilities
  TransportProtocol,
  Extensions,
  ExtensionURI,
  MySchema,
  JSONRPCMessage,
  JSONRPCRequest,
  JSONRPCResponse,
  JSONRPCSuccessResponse,
  JSONRPCError,
  // Aggregates
  A2AResponse,
  SendMessageResponse,
  SendStreamingMessageResponse,
  GetTaskResponse,
  CancelTaskResponse,
  GetTaskPushNotificationConfigResponse,
  SetTaskPushNotificationConfigResponse,
  DeleteTaskPushNotificationConfigResponse,
  ListTaskPushNotificationConfigResponse,
  GetAuthenticatedExtendedCardResponse,
} from "@a2a-js/sdk";

// Custom types not in SDK (AGenNext extensions)
export interface ApprovalRequest {
  taskId: string;
  agentName: string;
  question: string;
  context?: string;
  options?: string[];
  createdAt: string;
  expiresAt?: string;
}

export interface TaskSubmission {
  agentUrl: string;
  message: string;
  sessionId?: string;
  metadata?: Record<string, unknown>;
}

// Extended AgentCard with AGenNext-specific fields  
// Full field list combining SDK fields + AGenNext extensions
export interface AgentCardExtended {
  // A2A SDK fields
  capabilities?: AgentCapabilities;
  defaultInputModes?: string[];
  defaultOutputModes?: string[];
  // AGenNext/legacy compatibility fields
  url?: string;
  name?: string;
  description?: string;
  version?: string;
  provider?: { organization: string; url?: string };
  skills?: AgentSkill[];
  framework?: "openai" | "crewai" | "google-adk" | "langgraph" | "bedrock" | "anthropic" | "salesforce" | "custom";
  avgCompletionMs?: number;
  requiresApproval?: boolean;
}

// Bridge type for SSE stream events (our custom format)
// This matches the backend's simpler event structure
export interface TaskStreamEvent {
  id?: string;
  type: "status" | "artifact" | "error";
  taskId: string;
  status?: {
    state: TaskState;
    message?: {
      role?: string;
      parts?: Array<{ type: string; text?: string }>;
    };
    timestamp?: string;
  };
  artifact?: {
    name?: string;
    index?: number;
    parts?: Array<{ type: string; text?: string }>;
  };
  final?: boolean;
  error?: { code: number; message: string };
}
