import os

import pytest

import kozmochain
import kozmochain.embedder.gpt4all
import kozmochain.embedder.huggingface
import kozmochain.embedder.openai
import kozmochain.embedder.vertexai
import kozmochain.llm.anthropic
import kozmochain.llm.openai
import kozmochain.vectordb.chroma
import kozmochain.vectordb.elasticsearch
import kozmochain.vectordb.opensearch
from kozmochain.factory import EmbedderFactory, LlmFactory, VectorDBFactory


class TestFactories:
    @pytest.mark.parametrize(
        "provider_name, config_data, expected_class",
        [
            ("openai", {}, kozmochain.llm.openai.OpenAILlm),
            ("anthropic", {}, kozmochain.llm.anthropic.AnthropicLlm),
        ],
    )
    def test_llm_factory_create(self, provider_name, config_data, expected_class):
        os.environ["ANTHROPIC_API_KEY"] = "test_api_key"
        os.environ["OPENAI_API_KEY"] = "test_api_key"
        os.environ["OPENAI_API_BASE"] = "test_api_base"
        llm_instance = LlmFactory.create(provider_name, config_data)
        assert isinstance(llm_instance, expected_class)

    @pytest.mark.parametrize(
        "provider_name, config_data, expected_class",
        [
            ("gpt4all", {}, kozmochain.embedder.gpt4all.GPT4AllEmbedder),
            (
                "huggingface",
                {"model": "sentence-transformers/all-mpnet-base-v2", "vector_dimension": 768},
                kozmochain.embedder.huggingface.HuggingFaceEmbedder,
            ),
            ("vertexai", {"model": "textembedding-gecko"}, kozmochain.embedder.vertexai.VertexAIEmbedder),
            ("openai", {}, kozmochain.embedder.openai.OpenAIEmbedder),
        ],
    )
    def test_embedder_factory_create(self, mocker, provider_name, config_data, expected_class):
        mocker.patch("kozmochain.embedder.vertexai.VertexAIEmbedder", autospec=True)
        embedder_instance = EmbedderFactory.create(provider_name, config_data)
        assert isinstance(embedder_instance, expected_class)

    @pytest.mark.parametrize(
        "provider_name, config_data, expected_class",
        [
            ("chroma", {}, kozmochain.vectordb.chroma.ChromaDB),
            (
                "opensearch",
                {"opensearch_url": "http://localhost:9200", "http_auth": ("admin", "admin")},
                kozmochain.vectordb.opensearch.OpenSearchDB,
            ),
            ("elasticsearch", {"es_url": "http://localhost:9200"}, kozmochain.vectordb.elasticsearch.ElasticsearchDB),
        ],
    )
    def test_vectordb_factory_create(self, mocker, provider_name, config_data, expected_class):
        mocker.patch("kozmochain.vectordb.opensearch.OpenSearchDB", autospec=True)
        vectordb_instance = VectorDBFactory.create(provider_name, config_data)
        assert isinstance(vectordb_instance, expected_class)
