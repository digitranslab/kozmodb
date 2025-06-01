import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface LLMConfig {
  model: string;
  temperature: number;
  max_tokens: number;
  api_key?: string;
  ollama_base_url?: string;
}

export interface LLMProvider {
  provider: string;
  config: LLMConfig;
}

export interface EmbedderConfig {
  model: string;
  api_key?: string;
  ollama_base_url?: string;
}

export interface EmbedderProvider {
  provider: string;
  config: EmbedderConfig;
}

export interface KozmodbConfig {
  llm?: LLMProvider;
  embedder?: EmbedderProvider;
}

export interface KozMemoryConfig {
  custom_instructions?: string | null;
}

export interface ConfigState {
  kozmemory: KozMemoryConfig;
  kozmodb: KozmodbConfig;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

const initialState: ConfigState = {
  kozmemory: {
    custom_instructions: null,
  },
  kozmodb: {
    llm: {
      provider: 'openai',
      config: {
        model: 'gpt-4o-mini',
        temperature: 0.1,
        max_tokens: 2000,
        api_key: 'env:OPENAI_API_KEY',
      },
    },
    embedder: {
      provider: 'openai',
      config: {
        model: 'text-embedding-3-small',
        api_key: 'env:OPENAI_API_KEY',
      },
    },
  },
  status: 'idle',
  error: null,
};

const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    setConfigLoading: (state) => {
      state.status = 'loading';
      state.error = null;
    },
    setConfigSuccess: (state, action: PayloadAction<{ kozmemory?: KozMemoryConfig; kozmodb: KozmodbConfig }>) => {
      if (action.payload.kozmemory) {
        state.kozmemory = action.payload.kozmemory;
      }
      state.kozmodb = action.payload.kozmodb;
      state.status = 'succeeded';
      state.error = null;
    },
    setConfigError: (state, action: PayloadAction<string>) => {
      state.status = 'failed';
      state.error = action.payload;
    },
    updateKozMemory: (state, action: PayloadAction<KozMemoryConfig>) => {
      state.kozmemory = action.payload;
    },
    updateLLM: (state, action: PayloadAction<LLMProvider>) => {
      state.kozmodb.llm = action.payload;
    },
    updateEmbedder: (state, action: PayloadAction<EmbedderProvider>) => {
      state.kozmodb.embedder = action.payload;
    },
    updateKozmodbConfig: (state, action: PayloadAction<KozmodbConfig>) => {
      state.kozmodb = action.payload;
    },
  },
});

export const {
  setConfigLoading,
  setConfigSuccess,
  setConfigError,
  updateKozMemory,
  updateLLM,
  updateEmbedder,
  updateKozmodbConfig,
} = configSlice.actions;

export default configSlice.reducer; 