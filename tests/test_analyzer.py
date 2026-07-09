import json
from datetime import datetime
from unittest.mock import Mock

import pytest

from app.ai.analyzer import Analyzer
from app.ai.exceptions import LLMClientError
from app.models.analysis import Analysis
from app.models.article import Article


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture
def mock_client() -> Mock:
    """
    Mock LLM client.
    """
    return Mock()


@pytest.fixture
def analyzer(
    mock_client: Mock,
) -> Analyzer:
    """
    Analyzer under test.
    """
    return Analyzer(mock_client)


@pytest.fixture
def article() -> Article:
    """
    Sample article used throughout the tests.
    """
    return Article(
        id="article-1",
        title="NASA Announces New Artemis Timeline",
        url="https://example.com/article",
        published_at=datetime.now(),
        retrieved_at=datetime.now(),
        source="Example News",
        author="John Doe",
        content=(
            "NASA announced an updated launch schedule "
            "for the Artemis program."
        ),
        summary=(
            "NASA updated its Artemis launch schedule."
        ),
    )


@pytest.fixture
def valid_response() -> str:
    """
    Valid JSON response returned by the LLM.
    """
    return json.dumps(
        {
            "headline": "NASA Updates Artemis Timeline",
            "primary_event":
                "NASA announced a revised Artemis schedule.",
            "topics": [
                "Space",
                "Science",
            ],
            "people": [
                "Bill Nelson",
            ],
            "organizations": [
                "NASA",
            ],
            "locations": [
                "United States",
            ],
            "summary":
                "NASA released an updated timeline "
                "for future Artemis missions.",
            "political_lean": "Center",
            "bias_score": 0.0,
            "emotional_tone": "Neutral",
            "confidence": 0.95,
            "reasoning":
                "The article reports factual information "
                "without ideological framing.",
        }
    )


@pytest.fixture
def analysis(
    analyzer: Analyzer,
    valid_response: str,
) -> Analysis:
    """
    Parsed Analysis object.
    """
    return analyzer._parse_response(
        "article-1",
        valid_response,
    )

# ------------------------------------------------------------------
# _normalize_list()
# ------------------------------------------------------------------


def test_normalize_list_returns_empty_list_for_none(
    analyzer: Analyzer,
) -> None:
    """
    None should normalize to an empty list.
    """

    result = analyzer._normalize_list(None)

    assert result == []


def test_normalize_list_returns_empty_list_for_empty_string(
    analyzer: Analyzer,
) -> None:
    """
    Empty strings should normalize to an empty list.
    """

    result = analyzer._normalize_list("")

    assert result == []


def test_normalize_list_wraps_single_string(
    analyzer: Analyzer,
) -> None:
    """
    A single string should become a one-item list.
    """

    result = analyzer._normalize_list("NASA")

    assert result == ["NASA"]


def test_normalize_list_strips_whitespace(
    analyzer: Analyzer,
) -> None:
    """
    Leading and trailing whitespace should be removed.
    """

    result = analyzer._normalize_list("   NASA   ")

    assert result == ["NASA"]


def test_normalize_list_cleans_list_items(
    analyzer: Analyzer,
) -> None:
    """
    List items should be stripped and empty values removed.
    """

    result = analyzer._normalize_list(
        [
            " NASA ",
            "",
            " ",
            "SpaceX",
            "  ESA",
        ]
    )

    assert result == [
        "NASA",
        "SpaceX",
        "ESA",
    ]


def test_normalize_list_converts_non_string_values(
    analyzer: Analyzer,
) -> None:
    """
    Non-string values should be converted to strings.
    """

    result = analyzer._normalize_list(
        [
            42,
            True,
            3.14,
        ]
    )

    assert result == [
        "42",
        "True",
        "3.14",
    ]


def test_normalize_list_converts_single_non_string(
    analyzer: Analyzer,
) -> None:
    """
    A non-list value should become a single-item string list.
    """

    result = analyzer._normalize_list(42)

    assert result == ["42"]

# ------------------------------------------------------------------
# _parse_response()
# ------------------------------------------------------------------


def test_parse_response_returns_analysis(
    analyzer: Analyzer,
    valid_response: str,
) -> None:
    """
    A valid LLM response should produce an Analysis object.
    """

    analysis = analyzer._parse_response(
        "article-1",
        valid_response,
    )

    assert isinstance(analysis, Analysis)

    assert analysis.article_id == "article-1"
    assert analysis.headline == "NASA Updates Artemis Timeline"
    assert analysis.primary_event == (
        "NASA announced a revised Artemis schedule."
    )
    assert analysis.summary.startswith("NASA released")
    assert analysis.bias_score == 0.0
    assert analysis.confidence == 0.95

def test_parse_response_normalizes_lists(
    analyzer: Analyzer,
) -> None:
    """
    String values should be normalized into lists.
    """

    response = json.dumps(
        {
            "headline": "Headline",
            "primary_event": "Event",
            "topics": "Space",
            "people": "Bill Nelson",
            "organizations": "NASA",
            "locations": "United States",
            "summary": "Summary",
            "political_lean": "Center",
            "bias_score": 0.0,
            "emotional_tone": "Neutral",
            "confidence": 1.0,
            "reasoning": "Reason",
        }
    )

    analysis = analyzer._parse_response(
        "article-1",
        response,
    )

    assert analysis.topics == ["Space"]
    assert analysis.people == ["Bill Nelson"]
    assert analysis.organizations == ["NASA"]
    assert analysis.locations == ["United States"]

def test_parse_response_removes_duplicates(
    analyzer: Analyzer,
) -> None:
    """
    Duplicate list values should be removed.
    """

    response = json.dumps(
        {
            "headline": "Headline",
            "primary_event": "Event",
            "topics": [
                "Space",
                "Science",
                "Space",
            ],
            "people": [
                "Bill Nelson",
                "Bill Nelson",
            ],
            "organizations": [
                "NASA",
                "NASA",
            ],
            "locations": [
                "United States",
                "United States",
            ],
            "summary": "Summary",
            "political_lean": "Center",
            "bias_score": 0.0,
            "emotional_tone": "Neutral",
            "confidence": 1.0,
            "reasoning": "Reason",
        }
    )

    analysis = analyzer._parse_response(
        "article-1",
        response,
    )

    assert analysis.topics == [
        "Science",
        "Space",
    ]

    assert analysis.people == [
        "Bill Nelson",
    ]

    assert analysis.organizations == [
        "NASA",
    ]

    assert analysis.locations == [
        "United States",
    ]

def test_parse_response_title_cases_values(
    analyzer: Analyzer,
) -> None:
    """
    Political lean and emotional tone should be title-cased.
    """

    response = json.dumps(
        {
            "headline": "Headline",
            "primary_event": "Event",
            "topics": [],
            "people": [],
            "organizations": [],
            "locations": [],
            "summary": "Summary",
            "political_lean": "lean left",
            "bias_score": -0.3,
            "emotional_tone": "neutral",
            "confidence": 0.87,
            "reasoning": "Reason",
        }
    )

    analysis = analyzer._parse_response(
        "article-1",
        response,
    )

    assert analysis.political_lean == "Lean Left"
    assert analysis.emotional_tone == "Neutral"

# ------------------------------------------------------------------
# _parse_response() Exceptions
# ------------------------------------------------------------------


def test_parse_response_raises_for_invalid_json(
    analyzer: Analyzer,
) -> None:
    """
    Invalid JSON should raise an LLMClientError.
    """

    with pytest.raises(LLMClientError):
        analyzer._parse_response(
            "article-1",
            "This is not JSON.",
        )


def test_parse_response_raises_when_headline_missing(
    analyzer: Analyzer,
) -> None:
    """
    Missing required fields should raise an LLMClientError.
    """

    response = json.dumps(
        {
            "primary_event": "Event",
            "topics": [],
            "people": [],
            "organizations": [],
            "locations": [],
            "summary": "Summary",
            "political_lean": "Center",
            "bias_score": 0.0,
            "emotional_tone": "Neutral",
            "confidence": 0.90,
            "reasoning": "Reason",
        }
    )

    with pytest.raises(LLMClientError):
        analyzer._parse_response(
            "article-1",
            response,
        )


def test_parse_response_raises_for_invalid_bias_score(
    analyzer: Analyzer,
) -> None:
    """
    Bias score must be between -1.0 and 1.0.
    """

    response = json.dumps(
        {
            "headline": "Headline",
            "primary_event": "Event",
            "topics": [],
            "people": [],
            "organizations": [],
            "locations": [],
            "summary": "Summary",
            "political_lean": "Center",
            "bias_score": 5.0,
            "emotional_tone": "Neutral",
            "confidence": 0.95,
            "reasoning": "Reason",
        }
    )

    with pytest.raises(LLMClientError):
        analyzer._parse_response(
            "article-1",
            response,
        )


def test_parse_response_raises_for_invalid_confidence(
    analyzer: Analyzer,
) -> None:
    """
    Confidence must be between 0.0 and 1.0.
    """

    response = json.dumps(
        {
            "headline": "Headline",
            "primary_event": "Event",
            "topics": [],
            "people": [],
            "organizations": [],
            "locations": [],
            "summary": "Summary",
            "political_lean": "Center",
            "bias_score": 0.0,
            "emotional_tone": "Neutral",
            "confidence": 2.5,
            "reasoning": "Reason",
        }
    )

    with pytest.raises(LLMClientError):
        analyzer._parse_response(
            "article-1",
            response,
        )


def test_parse_response_accepts_null_optional_values(
    analyzer: Analyzer,
) -> None:
    """
    Optional values may be null.
    """

    response = json.dumps(
        {
            "headline": "Headline",
            "primary_event": "Event",
            "topics": [],
            "people": [],
            "organizations": [],
            "locations": [],
            "summary": "Summary",
            "political_lean": None,
            "bias_score": None,
            "emotional_tone": None,
            "confidence": None,
            "reasoning": None,
        }
    )

    analysis = analyzer._parse_response(
        "article-1",
        response,
    )

    assert analysis.bias_score is None
    assert analysis.confidence is None
    assert analysis.political_lean is None
    assert analysis.emotional_tone is None

# ------------------------------------------------------------------
# _build_prompt()
# ------------------------------------------------------------------


def test_build_prompt_contains_article_information(
    analyzer: Analyzer,
    article: Article,
) -> None:
    """
    Prompt should include article metadata.
    """

    prompt = analyzer._build_prompt(article)

    assert article.title in prompt
    assert article.source in prompt
    assert article.content in prompt


def test_build_prompt_contains_system_prompt(
    analyzer: Analyzer,
    article: Article,
) -> None:
    """
    Prompt should contain system instructions.
    """

    prompt = analyzer._build_prompt(article)

    assert "You are an impartial news analyst." in prompt
    assert "Return ONLY valid JSON." in prompt


def test_build_prompt_contains_json_schema(
    analyzer: Analyzer,
    article: Article,
) -> None:
    """
    Prompt should include the expected JSON schema.
    """

    prompt = analyzer._build_prompt(article)

    assert '"headline"' in prompt
    assert '"primary_event"' in prompt
    assert '"topics"' in prompt
    assert '"people"' in prompt
    assert '"organizations"' in prompt
    assert '"locations"' in prompt

# ------------------------------------------------------------------
# analyze()
# ------------------------------------------------------------------


def test_analyze_returns_analysis(
    analyzer: Analyzer,
    mock_client: Mock,
    article: Article,
    valid_response: str,
) -> None:
    """
    Analyzer should return an Analysis object when the LLM succeeds.
    """

    mock_client.generate.return_value = valid_response

    analysis = analyzer.analyze(article)

    assert isinstance(analysis, Analysis)

    mock_client.generate.assert_called_once()

    assert analysis.article_id == article.id
    assert analysis.headline == "NASA Updates Artemis Timeline"


def test_analyze_passes_prompt_to_llm(
    analyzer: Analyzer,
    mock_client: Mock,
    article: Article,
    valid_response: str,
) -> None:
    """
    Analyzer should send the generated prompt to the LLM.
    """

    mock_client.generate.return_value = valid_response

    analyzer.analyze(article)

    args, _ = mock_client.generate.call_args

    prompt = args[0]

    assert article.title in prompt
    assert article.content in prompt
    assert article.source in prompt


def test_analyze_propagates_llm_client_error(
    analyzer: Analyzer,
    mock_client: Mock,
    article: Article,
) -> None:
    """
    LLMClientError should be re-raised.
    """

    mock_client.generate.side_effect = LLMClientError(
        "OpenAI failed."
    )

    with pytest.raises(LLMClientError):
        analyzer.analyze(article)


def test_analyze_raises_when_response_is_invalid(
    analyzer: Analyzer,
    mock_client: Mock,
    article: Article,
) -> None:
    """
    Invalid JSON should raise an LLMClientError.
    """

    mock_client.generate.return_value = (
        "Definitely not JSON."
    )

    with pytest.raises(LLMClientError):
        analyzer.analyze(article)


def test_analyze_calls_generate_once(
    analyzer: Analyzer,
    mock_client: Mock,
    article: Article,
    valid_response: str,
) -> None:
    """
    The LLM should only be called once per article.
    """

    mock_client.generate.return_value = valid_response

    analyzer.analyze(article)

    assert mock_client.generate.call_count == 1


def test_analyze_returns_expected_analysis_values(
    analyzer: Analyzer,
    mock_client: Mock,
    article: Article,
    valid_response: str,
) -> None:
    """
    Parsed Analysis should contain expected values.
    """

    mock_client.generate.return_value = valid_response

    analysis = analyzer.analyze(article)

    assert analysis.topics == [
        "Science",
        "Space",
    ]

    assert analysis.people == [
        "Bill Nelson",
    ]

    assert analysis.organizations == [
        "NASA",
    ]

    assert analysis.locations == [
        "United States",
    ]

    assert analysis.bias_score == 0.0
    assert analysis.confidence == 0.95

