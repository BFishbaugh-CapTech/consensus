import os
from unittest.mock import Mock, patch

import pytest

from app.ai.exceptions import LLMClientError
from app.ai.llm_client import LLMClient

# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture
def mock_openai():
    with patch("app.ai.llm_client.OpenAI") as mock:
        yield mock


@pytest.fixture
def client(
    mock_openai,
):
    return LLMClient(
        api_key="unit-test-key",
        model="gpt-5",
    )

# ------------------------------------------------------------------
# Constructor
# ------------------------------------------------------------------


def test_constructor_sets_model(
    client: LLMClient,
):
    assert client.model == "gpt-5"


def test_constructor_uses_environment_model(
    mock_openai,
    monkeypatch,
):
    monkeypatch.setenv(
        "OPENAI_MODEL",
        "gpt-5-mini",
    )

    client = LLMClient(
        api_key="abc",
    )

    assert client.model == "gpt-5-mini"


def test_constructor_raises_without_api_key(
    monkeypatch,
):
    monkeypatch.delenv(
        "OPENAI_API_KEY",
        raising=False,
    )

    with pytest.raises(RuntimeError):
        LLMClient()

# ------------------------------------------------------------------
# _build_request()
# ------------------------------------------------------------------


def test_build_request(
    client: LLMClient,
):
    request = client._build_request(
        "Hello"
    )

    assert request["model"] == "gpt-5"
    assert request["input"] == "Hello"

# ------------------------------------------------------------------
# generate()
# ------------------------------------------------------------------


def test_generate_returns_response(
    client: LLMClient,
):
    response = Mock()
    response.output_text = "Hello"

    client.client.responses.create.return_value = (
        response
    )

    text = client.generate(
        "Prompt"
    )

    assert text == "Hello"


def test_generate_strips_whitespace(
    client: LLMClient,
):
    response = Mock()
    response.output_text = (
        "   Hello GPT   "
    )

    client.client.responses.create.return_value = (
        response
    )

    assert (
        client.generate("Prompt")
        == "Hello GPT"
    )

def test_generate_raises_on_empty_response(
    client: LLMClient,
):
    response = Mock()
    response.output_text = "   "

    client.client.responses.create.return_value = (
        response
    )

    with pytest.raises(
        LLMClientError
    ):
        client.generate(
            "Prompt"
        )

def test_generate_wraps_openai_exception(
    client: LLMClient,
):
    client.client.responses.create.side_effect = (
        Exception("Boom")
    )

    with pytest.raises(
        LLMClientError
    ):
        client.generate(
            "Prompt"
        )

def test_generate_reraises_llm_client_error(
    client: LLMClient,
):
    client.client.responses.create.side_effect = (
        LLMClientError(
            "Already wrapped."
        )
    )

    with pytest.raises(
        LLMClientError
    ):
        client.generate(
            "Prompt"
        )

def test_generate_calls_openai_once(
    client: LLMClient,
):
    response = Mock()
    response.output_text = "Hello"

    client.client.responses.create.return_value = (
        response
    )

    client.generate(
        "Prompt"
    )

    client.client.responses.create.assert_called_once()

