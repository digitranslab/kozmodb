import { withoutTrailingSlash } from '@ai-sdk/provider-utils'

import { KozmodbGenericLanguageModel } from './kozmodb-generic-language-model'
import { KozmodbChatModelId, KozmodbChatSettings } from './kozmodb-types'
import { KozmodbProviderSettings } from './kozmodb-provider'

export class Kozmodb {
  readonly baseURL: string
  readonly headers?: any

  constructor(options: KozmodbProviderSettings = {
    provider: 'openai',
  }) {
    this.baseURL =
      withoutTrailingSlash(options.baseURL) ?? 'http://127.0.0.1:11434/api'

    this.headers = options.headers
  }

  private get baseConfig() {
    return {
      baseURL: this.baseURL,
      headers: this.headers,
    }
  }

  chat(modelId: KozmodbChatModelId, settings: KozmodbChatSettings = {}) {
    return new KozmodbGenericLanguageModel(modelId, settings, {
      provider: 'openai',
      modelType: 'chat',
      ...this.baseConfig,
    })
  }

  completion(modelId: KozmodbChatModelId, settings: KozmodbChatSettings = {}) {
    return new KozmodbGenericLanguageModel(modelId, settings, {
      provider: 'openai',
      modelType: 'completion',
      ...this.baseConfig,
    })
  }
}