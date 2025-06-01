import { MemoryClient } from "./kozmodb";
import type * as MemoryTypes from "./kozmodb.types";

// Re-export all types from kozmodb.types
export type {
  MemoryOptions,
  ProjectOptions,
  Memory,
  MemoryHistory,
  MemoryUpdateBody,
  ProjectResponse,
  PromptUpdatePayload,
  SearchOptions,
  Webhook,
  WebhookPayload,
  Messages,
  Message,
  AllUsers,
  User,
  FeedbackPayload,
  Feedback,
} from "./kozmodb.types";

// Export the main client
export { MemoryClient };
export default MemoryClient;
