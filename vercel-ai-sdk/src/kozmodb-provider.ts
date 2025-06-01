import { LanguageModelV1, ProviderV1 } from "@ai-sdk/provider";
import { loadApiKey, withoutTrailingSlash } from "@ai-sdk/provider-utils";
import { KozmodbChatModelId, KozmodbChatSettings, KozmodbConfig } from "./kozmodb-types";
import { OpenAIProviderSettings } from "@ai-sdk/openai";
import { KozmodbGenericLanguageModel } from "./kozmodb-generic-language-model";
import { OpenAIChatSettings } from "@ai-sdk/openai/internal";
import { AnthropicMessagesSettings } from "@ai-sdk/anthropic/internal";
import { AnthropicProviderSettings } from "@ai-sdk/anthropic";

export interface KozmodbProvider extends ProviderV1 {
  (modelId: KozmodbChatModelId, settings?: KozmodbChatSettings): LanguageModelV1;

  chat(modelId: KozmodbChatModelId, settings?: KozmodbChatSettings): LanguageModelV1;
  completion(modelId: KozmodbChatModelId, settings?: KozmodbChatSettings): LanguageModelV1;

  languageModel(
    modelId: KozmodbChatModelId,
    settings?: KozmodbChatSettings
  ): LanguageModelV1;
}

export interface KozmodbProviderSettings
  extends OpenAIChatSettings,
    AnthropicMessagesSettings {
  baseURL?: string;
  /**
   * Custom fetch implementation. You can use it as a middleware to intercept
   * requests or to provide a custom fetch implementation for e.g. testing
   */
  fetch?: typeof fetch;
  /**
   * @internal
   */
  generateId?: () => string;
  /**
   * Custom headers to include in the requests.
   */
  headers?: Record<string, string>;
  name?: string;
  mem0ApiKey?: string;
  apiKey?: string;
  provider?: string;
  modelType?: "completion" | "chat";
  mem0Config?: KozmodbConfig;

  /**
   * The configuration for the provider.
   */
  config?: OpenAIProviderSettings | AnthropicProviderSettings;
}

export function createKozmodb(
  options: KozmodbProviderSettings = {
    provider: "openai",
  }
): KozmodbProvider {
  const baseURL =
    withoutTrailingSlash(options.baseURL) ?? "http://api.openai.com";
  const getHeaders = () => ({
    ...options.headers,
  });

  const createGenericModel = (
    modelId: KozmodbChatModelId,
    settings: KozmodbChatSettings = {}
  ) =>
    new KozmodbGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        mem0ApiKey: options.mem0ApiKey,
        apiKey: options.apiKey,
        mem0Config: options.mem0Config,
      },
      options.config
    );

  const createCompletionModel = (
    modelId: KozmodbChatModelId,
    settings: KozmodbChatSettings = {}
  ) =>
    new KozmodbGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        mem0ApiKey: options.mem0ApiKey,
        apiKey: options.apiKey,
        mem0Config: options.mem0Config,
        modelType: "completion",
      },
      options.config
    );

  const createChatModel = (
    modelId: KozmodbChatModelId,
    settings: KozmodbChatSettings = {}
  ) =>
    new KozmodbGenericLanguageModel(
      modelId,
      settings,
      {
        baseURL,
        fetch: options.fetch,
        headers: getHeaders(),
        provider: options.provider || "openai",
        name: options.name,
        mem0ApiKey: options.mem0ApiKey,
        apiKey: options.apiKey,
        mem0Config: options.mem0Config,
        modelType: "completion",
      },
      options.config
    );

  const provider = function (
    modelId: KozmodbChatModelId,
    settings: KozmodbChatSettings = {}
  ) {
    if (new.target) {
      throw new Error(
        "The Kozmodb model function cannot be called with the new keyword."
      );
    }

    return createGenericModel(modelId, settings);
  };

  provider.languageModel = createGenericModel;
  provider.completion = createCompletionModel;
  provider.chat = createChatModel;

  return provider as unknown as KozmodbProvider;
}

export const kozmodb = createKozmodb();
