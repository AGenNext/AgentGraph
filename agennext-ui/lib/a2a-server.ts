// lib/a2a-server.ts
// A2A Server components from @a2a-js/sdk
// Re-export all server components for direct usage

// Server runtime components
export {
  DefaultRequestHandler,
  InMemoryTaskStore,
  InMemoryPushNotificationStore,
  JsonRpcTransportHandler,
} from "@a2a-js/sdk/server";

// Server types (re-export from main SDK)
export type {
  AgentCard,
  Task,
  TaskState,
  TaskStatus,
  TaskStatusUpdateEvent,
  TaskArtifactUpdateEvent,
  Message,
  MessageSendParams,
  TaskQueryParams,
  TaskIdParams,
  PushNotificationConfig,
  GetTaskPushNotificationConfigParams,
  ListTaskPushNotificationConfigParams,
  DeleteTaskPushNotificationConfigParams,
} from "@a2a-js/sdk";

// Server-specific types
export type {
  User,
  UnauthenticatedUser,
  ServerCallContext,
  TaskStore,
  PushNotificationStore,
  ExecutionEventBus,
  AgentExecutionEvent,
  A2ARequestHandler,
  ExtendedAgentCardProvider,
} from "@a2a-js/sdk/server";