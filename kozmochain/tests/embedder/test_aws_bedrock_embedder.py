from unittest.mock import patch

from kozmochain.config.embedder.aws_bedrock import AWSBedrockEmbedderConfig
from kozmochain.embedder.aws_bedrock import AWSBedrockEmbedder


def test_aws_bedrock_embedder_with_model():
    config = AWSBedrockEmbedderConfig(
        model="test-model",
        model_kwargs={"param": "value"},
        vector_dimension=1536,
    )
    with patch("kozmochain.embedder.aws_bedrock.BedrockEmbeddings") as mock_embeddings:
        embedder = AWSBedrockEmbedder(config=config)
        assert embedder.config.model == "test-model"
        assert embedder.config.model_kwargs == {"param": "value"}
        assert embedder.config.vector_dimension == 1536
        mock_embeddings.assert_called_once_with(
            model_id="test-model",
            model_kwargs={"param": "value"},
        )
