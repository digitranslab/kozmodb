from unittest.mock import Mock, patch

import pytest

try:
    from kozmodb.proxy.main import Chat, Completions, Kozmodb
    proxy_available = True
except (ImportError, AttributeError):
    proxy_available = False

pytestmark = pytest.mark.skipif(not proxy_available, reason="Proxy dependencies not available or have compatibility issues")

from kozmodb import Memory, MemoryClient


@pytest.fixture
def mock_memory_client():
    mock_client = Mock(spec=MemoryClient)
    mock_client.user_email = None
    return mock_client


@pytest.fixture
def mock_openai_embedding_client():
    with patch("kozmodb.embeddings.openai.OpenAI") as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_openai_llm_client():
    with patch("kozmodb.llms.openai.OpenAI") as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_litellm():
    with patch("kozmodb.proxy.main.litellm") as mock:
        yield mock


def test_kozmodb_initialization_with_api_key(mock_openai_embedding_client, mock_openai_llm_client):
    kozmodb = Kozmodb()
    assert isinstance(kozmodb.kozmodb_client, Memory)
    assert isinstance(kozmodb.chat, Chat)


def test_kozmodb_initialization_with_config():
    config = {"some_config": "value"}
    with patch("kozmodb.Memory.from_config") as mock_from_config:
        kozmodb = Kozmodb(config=config)
        mock_from_config.assert_called_once_with(config)
        assert isinstance(kozmodb.chat, Chat)


def test_kozmodb_initialization_without_params(mock_openai_embedding_client, mock_openai_llm_client):
    kozmodb = Kozmodb()
    assert isinstance(kozmodb.kozmodb_client, Memory)
    assert isinstance(kozmodb.chat, Chat)


def test_chat_initialization(mock_memory_client):
    chat = Chat(mock_memory_client)
    assert isinstance(chat.completions, Completions)


def test_completions_create(mock_memory_client, mock_litellm):
    completions = Completions(mock_memory_client)

    messages = [{"role": "user", "content": "Hello, how are you?"}]
    mock_memory_client.search.return_value = [{"memory": "Some relevant memory"}]
    mock_litellm.completion.return_value = {"choices": [{"message": {"content": "I'm doing well, thank you!"}}]}
    mock_litellm.supports_function_calling.return_value = True

    response = completions.create(model="gpt-4o-mini", messages=messages, user_id="test_user", temperature=0.7)

    mock_memory_client.add.assert_called_once()
    mock_memory_client.search.assert_called_once()

    mock_litellm.completion.assert_called_once()
    call_args = mock_litellm.completion.call_args[1]
    assert call_args["model"] == "gpt-4o-mini"
    assert len(call_args["messages"]) == 2
    assert call_args["temperature"] == 0.7

    assert response == {"choices": [{"message": {"content": "I'm doing well, thank you!"}}]}


def test_completions_create_with_system_message(mock_memory_client, mock_litellm):
    completions = Completions(mock_memory_client)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
    ]
    mock_memory_client.search.return_value = [{"memory": "Some relevant memory"}]
    mock_litellm.completion.return_value = {"choices": [{"message": {"content": "I'm doing well, thank you!"}}]}
    mock_litellm.supports_function_calling.return_value = True

    completions.create(model="gpt-4o-mini", messages=messages, user_id="test_user")

    call_args = mock_litellm.completion.call_args[1]
    assert call_args["messages"][0]["role"] == "system"
    assert call_args["messages"][0]["content"] == "You are a helpful assistant."
