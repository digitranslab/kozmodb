import { useState } from 'react';
import { createKozmodb, getMemories } from '@kozmodb/vercel-ai-provider';
import { LanguageModelV1Prompt, streamText } from 'ai';
import { Message, Memory } from '@/types';
import { WELCOME_MESSAGE, INVALID_CONFIG_MESSAGE, ERROR_MESSAGE, AI_MODELS, Provider } from '@/constants/messages';

interface UseChatProps {
  user: string;
  kozmodbApiKey: string;
  openaiApiKey: string;
  provider: Provider;
}

interface UseChatReturn {
  messages: Message[];
  memories: Memory[];
  thinking: boolean;
  sendMessage: (content: string, fileData?: { type: string; data: string | Buffer }) => Promise<void>;
}

interface MemoryResponse {
  id: string;
  memory: string;
  updated_at: string;
  categories: string[];
}

type MessageContent = 
  | { type: 'text'; text: string }
  | { type: 'image'; image: string }
  | { type: 'file'; mimeType: string; data: Buffer };

interface PromptMessage {
  role: string;
  content: MessageContent[];
}

export const useChat = ({ user, kozmodbApiKey, openaiApiKey, provider }: UseChatProps): UseChatReturn => {
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE]);
  const [memories, setMemories] = useState<Memory[]>([]);
  const [thinking, setThinking] = useState(false);

  const kozmodb = createKozmodb({
    provider,
    kozmodbApiKey,
    apiKey: openaiApiKey,
  });

  const updateMemories = async (messages: LanguageModelV1Prompt) => {
    try {
      const fetchedMemories = await getMemories(messages, {
        user_id: user,
        kozmodbApiKey,
      });

      const newMemories = fetchedMemories.map((memory: MemoryResponse) => ({
        id: memory.id,
        content: memory.memory,
        timestamp: memory.updated_at,
        tags: memory.categories,
      }));
      setMemories(newMemories);
    } catch (error) {
      console.error('Error in getMemories:', error);
    }
  };

  const formatMessagesForPrompt = (messages: Message[]): PromptMessage[] => {
    return messages.map((message) => {
      const messageContent: MessageContent[] = [
        { type: 'text', text: message.content }
      ];

      if (message.image) {
        messageContent.push({
          type: 'image',
          image: message.image,
        });
      }

      if (message.audio) {
        messageContent.push({
          type: 'file',
          mimeType: 'audio/mpeg',
          data: message.audio as Buffer,
        });
      }

      return {
        role: message.sender,
        content: messageContent,
      };
    });
  };

  const sendMessage = async (content: string, fileData?: { type: string; data: string | Buffer }) => {
    if (!content.trim() && !fileData) return;

    if (!user) {
      const newMessage: Message = {
        id: Date.now().toString(),
        content,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, newMessage, INVALID_CONFIG_MESSAGE]);
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
      ...(fileData?.type.startsWith('image/') && { image: fileData.data.toString() }),
      ...(fileData?.type.startsWith('audio/') && { audio: fileData.data as Buffer }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setThinking(true);

    const messagesForPrompt = formatMessagesForPrompt([...messages, userMessage]);
    await updateMemories(messagesForPrompt as LanguageModelV1Prompt);

    try {
      const { textStream } = await streamText({
        model: kozmodb(AI_MODELS[provider], {
          user_id: user,
        }),
        messages: messagesForPrompt as LanguageModelV1Prompt,
      });

      const assistantMessageId = Date.now() + 1;
      const assistantMessage: Message = {
        id: assistantMessageId.toString(),
        content: '',
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      for await (const textPart of textStream) {
        assistantMessage.content += textPart;
        setThinking(false);

        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMessageId.toString()
              ? { ...msg, content: assistantMessage.content }
              : msg
          )
        );
      }
    } catch (error) {
      console.error('Error in sendMessage:', error);
      setMessages((prev) => [...prev, ERROR_MESSAGE]);
    } finally {
      setThinking(false);
    }
  };

  return {
    messages,
    memories,
    thinking,
    sendMessage,
  };
}; 