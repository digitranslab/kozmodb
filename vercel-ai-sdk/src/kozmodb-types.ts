import { KozmodbProviderSettings } from "./kozmodb-provider";
import { OpenAIChatSettings } from "@ai-sdk/openai/internal";
import { AnthropicMessagesSettings } from "@ai-sdk/anthropic/internal";
import {
  LanguageModelV1
} from "@ai-sdk/provider";

export type KozmodbChatModelId =
  | (string & NonNullable<unknown>);

export interface KozmodbConfigSettings {
  user_id?: string;
  app_id?: string;
  agent_id?: string;
  run_id?: string;
  org_name?: string;
  project_name?: string;
  org_id?: string;
  project_id?: string;
  metadata?: Record<string, any>;
  filters?: Record<string, any>;
  infer?: boolean;
  page?: number;
  page_size?: number;
  kozmodbApiKey?: string;
  top_k?: number;
  threshold?: number;
  rerank?: boolean;
  enable_graph?: boolean;
  output_format?: string;
}

export interface KozmodbChatConfig extends KozmodbConfigSettings, KozmodbProviderSettings {}

export interface KozmodbConfig extends KozmodbConfigSettings {}
export interface KozmodbChatSettings extends OpenAIChatSettings, AnthropicMessagesSettings, KozmodbConfigSettings {}

export interface KozmodbStreamResponse extends Awaited<ReturnType<LanguageModelV1['doStream']>> {
  memories: any;
}
