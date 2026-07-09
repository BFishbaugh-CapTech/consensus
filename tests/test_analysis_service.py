import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.models.analysis import Analysis
from app.models.article import Article
from app.services.analysis_service import AnalysisService

# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture
def mock_analyzer() -> Mock:
    return Mock()


@pytest.fixture
def service(
    mock_analyzer: Mock,
) -> AnalysisService:
    return AnalysisService(
        mock_analyzer,
    )


@pytest.fixture
def article() -> Article:
    return Article(
        id="article-1",
        title="Test Article",
        url="https://example.com",
        published_at=None,
        retrieved_at=None,
        source="Unit Test",
        author=None,
        content="Some content",
        summary="Summary",
    )


@pytest.fixture
def analysis() -> Analysis:
    return Analysis(
        article_id="article-1",
        headline="Headline",
        primary_event="Primary Event",
        summary="Summary",
        topics=["Politics"],
        people=["John Doe"],
        organizations=["NASA"],
        locations=["USA"],
        political_lean="Center",
        bias_score=0.0,
        emotional_tone="Neutral",
        confidence=0.95,
        reasoning="Reason",
    )

# ------------------------------------------------------------------
# analyze_articles()
# ------------------------------------------------------------------


def test_analyze_articles_returns_single_analysis(
    service: AnalysisService,
    mock_analyzer: Mock,
    article: Article,
    analysis: Analysis,
):
    mock_analyzer.analyze.return_value = analysis

    results = service.analyze_articles(
        [article]
    )

    assert len(results) == 1
    assert results[0] == analysis

    mock_analyzer.analyze.assert_called_once_with(
        article
    )


def test_analyze_articles_returns_multiple_results(
    service: AnalysisService,
    mock_analyzer: Mock,
    article: Article,
    analysis: Analysis,
):
    mock_analyzer.analyze.return_value = analysis

    articles = [
        article,
        article,
        article,
    ]

    results = service.analyze_articles(
        articles
    )

    assert len(results) == 3
    assert mock_analyzer.analyze.call_count == 3


def test_analyze_articles_returns_empty_list(
    service: AnalysisService,
):
    results = service.analyze_articles([])

    assert results == []


def test_analyze_articles_continues_after_failure(
    service: AnalysisService,
    mock_analyzer: Mock,
    article: Article,
    analysis: Analysis,
):
    mock_analyzer.analyze.side_effect = [
        analysis,
        Exception("Failure"),
        analysis,
    ]

    results = service.analyze_articles(
        [
            article,
            article,
            article,
        ]
    )

    assert len(results) == 2

# ------------------------------------------------------------------
# export_analysis_to_json()
# ------------------------------------------------------------------


def test_export_analysis_to_json(
    service: AnalysisService,
    analysis: Analysis,
    tmp_path: Path,
):
    output = tmp_path / "analysis.json"

    service.export_analysis_to_json(
        [analysis],
        str(output),
    )

    assert output.exists()

    data = json.loads(
        output.read_text()
    )

    assert len(data) == 1
    assert (
        data[0]["headline"]
        == "Headline"
    )


def test_export_analysis_to_json_empty_list(
    service: AnalysisService,
    tmp_path: Path,
):
    output = tmp_path / "analysis.json"

    service.export_analysis_to_json(
        [],
        str(output),
    )

    data = json.loads(
        output.read_text()
    )

    assert data == []

# ------------------------------------------------------------------
# _default_output_path()
# ------------------------------------------------------------------


def test_default_output_path_contains_data_directory(
    service: AnalysisService,
):
    path = service._default_output_path()

    assert path.startswith("data/")


def test_default_output_path_has_json_extension(
    service: AnalysisService,
):
    path = service._default_output_path()

    assert path.endswith(
        "Analysis.json"
    )

