/* eslint-disable camelcase */
import {
  LanguageModelV1,
  LanguageModelV1CallOptions,
  LanguageModelV1Message,
} from "@ai-sdk/provider";

import { KozmodbChatConfig, KozmodbChatModelId, KozmodbChatSettings, KozmodbConfigSettings, KozmodbStreamResponse } from "./kozmodb-types";
import { KozmodbClassSelector } from "./kozmodb-provider-selector";
import { KozmodbProviderSettings } from "./kozmodb-provider";
import { addMemories, getMemories, retrieveMemories } from "./kozmodb-utils";

const generateRandomId = () => {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

export class KozmodbGenericLanguageModel implements LanguageModelV1 {
  readonly specificationVersion = "v1";
  readonly defaultObjectGenerationMode = "json";
  readonly supportsImageUrls = false;

  constructor(
    public readonly modelId: KozmodbChatModelId,
    public readonly settings: KozmodbChatSettings,
    public readonly config: KozmodbChatConfig,
    public readonly provider_config?: KozmodbProviderSettings
  ) {
    this.provider = config.provider ?? "openai";
  }

  provider: string;

  private async processMemories(messagesPrompts: LanguageModelV1Message[], mem0Config: KozmodbConfigSettings) {
    try {
    // Add New Memories
    addMemories(messagesPrompts, mem0Config).then((res) => {
      return res;
    }).catch((e) => {
      console.error("Error while adding memories");
      return { memories: [], messagesPrompts: [] };
    });

    // Get Memories
    let memories = await getMemories(messagesPrompts, mem0Config);

    const mySystemPrompt = "These are the memories I have stored. Give more weightage to the question by users and try to answer that first. You have to modify your answer based on the memories I have provided. If the memories are irrelevant you can ignore them. Also don't reply to this section of the prompt, or the memories, they are only for your reference. The System prompt starts after text System Message: \n\n";

    const isGraphEnabled = mem0Config?.enable_graph;
  
    let memoriesText = "";
    let memoriesText2 = "";
    try {
      // @ts-ignore
      if (isGraphEnabled) {
        memoriesText = memories?.results?.map((memory: any) => {
          return `Memory: ${memory?.memory}\n\n`;
        }).join("\n\n");

        memoriesText2 = memories?.relations?.map((memory: any) => {
          return `Relation: ${memory?.source} -> ${memory?.relationship} -> ${memory?.target} \n\n`;
        }).join("\n\n");
      } else {
        memoriesText = memories?.map((memory: any) => {
          return `Memory: ${memory?.memory}\n\n`;
        }).join("\n\n");
      }
    } catch(e) {
      console.error("Error while parsing memories");
    }

    let graphPrompt = "";
    if (isGraphEnabled) {
      graphPrompt = `HERE ARE THE GRAPHS RELATIONS FOR THE PREFERENCES OF THE USER:\n\n ${memoriesText2}`;
    }

    const memoriesPrompt = `System Message: ${mySystemPrompt} ${memoriesText} ${graphPrompt} `;

    // System Prompt - The memories go as a system prompt
    const systemPrompt: LanguageModelV1Message = {
      role: "system",
      content: memoriesPrompt
    };

    // Add the system prompt to the beginning of the messages if there are memories
    if (memories?.length > 0) {
      messagesPrompts.unshift(systemPrompt);
    }

    if (isGraphEnabled) {
      memories = memories?.results;
    }

    return { memories, messagesPrompts };
    } catch(e) {
      console.error("Error while processing memories");
      return { memories: [], messagesPrompts };
    }
  }

  async doGenerate(options: LanguageModelV1CallOptions): Promise<Awaited<ReturnType<LanguageModelV1['doGenerate']>>> {
    try {   
      const provider = this.config.provider;
      const mem0_api_key = this.config.mem0ApiKey;
      
      const settings: KozmodbProviderSettings = {
        provider: provider,
        mem0ApiKey: mem0_api_key,
        apiKey: this.config.apiKey,
      }

      const mem0Config: KozmodbConfigSettings = {
        mem0ApiKey: mem0_api_key,
        ...this.config.mem0Config,
        ...this.settings,
      }

      const selector = new KozmodbClassSelector(this.modelId, settings, this.provider_config);
      
      let messagesPrompts = options.prompt;
      
      // Process memories and update prompts
      const { memories, messagesPrompts: updatedPrompts } = await this.processMemories(messagesPrompts, mem0Config);
      
      const model = selector.createProvider();

      const ans = await model.doGenerate({
        ...options,
        prompt: updatedPrompts,
      });
      
      // If there are no memories, return the original response
      if (!memories || memories?.length === 0) {
        return ans;
      }
      
      // Create sources array with existing sources
      const sources = [...(ans.sources || [])];
      
      // Add a combined source with all memories
      if (Array.isArray(memories) && memories?.length > 0) {
        sources.push({
          title: "Kozmodb Memories",
          sourceType: "url",
          id: "kozmodb-" + generateRandomId(),
          url: "https://app.kozmodb.ai",
          providerMetadata: {
            kozmodb: {
              memories: memories,
              memoriesText: memories?.map((memory: any) => memory?.memory).join("\n\n")
            }
          }
        });
        
        // Add individual memory sources for more detailed information
        memories?.forEach((memory: any) => {
          sources.push({
            title: memory.title || "Memory",
            sourceType: "url",
            id: "kozmodb-memory-" + generateRandomId(),
            url: "https://app.kozmodb.ai",
            providerMetadata: {
              kozmodb: {
                memory: memory,
                memoryText: memory?.memory
              }
            }
          });
        });
      }
 
      return {
        ...ans,
        sources
      };
    } catch (error) {
      // Handle errors properly
      console.error("Error in doGenerate:", error);
      throw new Error("Failed to generate response.");
    }
  }

  async doStream(options: LanguageModelV1CallOptions): Promise<Awaited<ReturnType<LanguageModelV1['doStream']>>> {
    try {
      const provider = this.config.provider;
      const mem0_api_key = this.config.mem0ApiKey;
      
      const settings: KozmodbProviderSettings = {
        provider: provider,
        mem0ApiKey: mem0_api_key,
        apiKey: this.config.apiKey,
        modelType: this.config.modelType,
      }

      const mem0Config: KozmodbConfigSettings = {
        mem0ApiKey: mem0_api_key,
        ...this.config.mem0Config,
        ...this.settings,
      }

      const selector = new KozmodbClassSelector(this.modelId, settings, this.provider_config);
      
      let messagesPrompts = options.prompt;
      
      // Process memories and update prompts
      const { memories, messagesPrompts: updatedPrompts } = await this.processMemories(messagesPrompts, mem0Config);

      const model = selector.createProvider();

      const streamResponse = await model.doStream({
        ...options,
        prompt: updatedPrompts,
      });

      // If there are no memories, return the original stream
      if (!memories || memories?.length === 0) {
        return streamResponse;
      }

      // Create a new stream that includes memory sources
      const originalStream = streamResponse.stream;
      
      // Create a transform stream that adds memory sources at the beginning
      const transformStream = new TransformStream({
        start(controller) {
          // Add source chunks for each memory at the beginning
          try {
            if (Array.isArray(memories) && memories?.length > 0) {
              // Create a single source that contains all memories
              controller.enqueue({
                type: 'source',
                source: {
                  title: "Kozmodb Memories",
                  sourceType: "url",
                  id: "kozmodb-" + generateRandomId(),
                  url: "https://app.kozmodb.ai",
                  providerMetadata: {
                    kozmodb: {
                      memories: memories,
                      memoriesText: memories?.map((memory: any) => memory?.memory).join("\n\n")
                    }
                  }
                }
              });
              
              // Also add individual memory sources for more detailed information
              memories?.forEach((memory: any) => {
                controller.enqueue({
                  type: 'source',
                  source: {
                    title: memory?.title || "Memory",
                    sourceType: "url",
                    id: "kozmodb-memory-" + generateRandomId(),
                    url: "https://app.kozmodb.ai",
                    providerMetadata: {
                      kozmodb: {
                        memory: memory,
                        memoryText: memory?.memory
                      }
                    }
                  }
                });
              });
            }
          } catch (error) {
            console.error("Error adding memory sources:", error);
          }
        },
        transform(chunk, controller) {
          // Pass through all chunks from the original stream
          controller.enqueue(chunk);
        }
      });

      // Pipe the original stream through our transform stream
      const enhancedStream = originalStream.pipeThrough(transformStream);

      // Return a new stream response with our enhanced stream
      return {
        stream: enhancedStream,
        rawCall: streamResponse.rawCall,
        rawResponse: streamResponse.rawResponse,
        request: streamResponse.request,
        warnings: streamResponse.warnings
      };
    } catch (error) {
      console.error("Error in doStream:", error);
      throw new Error("Streaming failed or method not implemented.");
    }
  }
}
