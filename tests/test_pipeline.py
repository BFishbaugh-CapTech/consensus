import pytest
from unittest.mock import Mock, patch

from app.pipeline import Pipeline


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture
def pipeline():
    with patch("app.pipeline.RSSService") as rss, \
         patch("app.pipeline.LLMClient"), \
         patch("app.pipeline.Analyzer"), \
         patch("app.pipeline.AnalysisService"):

        yield Pipeline()

# ------------------------------------------------------------------
# _fetch_articles()
# ------------------------------------------------------------------


def test_fetch_articles(
    pipeline,
):
    articles = [Mock(), Mock()]

    pipeline.rss_service.get_articles.return_value = (
        articles
    )

    results = pipeline._fetch_articles()

    assert results == articles

    pipeline.rss_service.get_articles.assert_called_once()

# ------------------------------------------------------------------
# _analyze_articles()
# ------------------------------------------------------------------


def test_analyze_articles(
    pipeline,
):
    articles = [Mock(), Mock()]
    analyses = [Mock(), Mock()]

    pipeline.analysis_service.analyze_articles.return_value = (
        analyses
    )

    results = pipeline._analyze_articles(
        articles
    )

    assert results == analyses

    pipeline.analysis_service.analyze_articles.assert_called_once_with(
        articles
    )

# ------------------------------------------------------------------
# _export_results()
# ------------------------------------------------------------------


def test_export_results(
    pipeline,
):
    articles = [Mock()]
    analyses = [Mock()]

    pipeline._export_results(
        articles,
        analyses,
    )

    pipeline.rss_service.export_articles_to_json.assert_called_once_with(
        articles
    )

    pipeline.analysis_service.export_analysis_to_json.assert_called_once_with(
        analyses
    )

# ------------------------------------------------------------------
# run()
# ------------------------------------------------------------------


def test_run_executes_pipeline(
    pipeline,
):
    articles = [Mock()]
    analyses = [Mock()]

    pipeline._fetch_articles = Mock(
        return_value=articles
    )

    pipeline._analyze_articles = Mock(
        return_value=analyses
    )

    pipeline._export_results = Mock()

    pipeline.run()

    pipeline._fetch_articles.assert_called_once()

    pipeline._analyze_articles.assert_called_once_with(
        articles
    )

    pipeline._export_results.assert_called_once_with(
        articles,
        analyses,
    )

def test_run_with_no_articles(
    pipeline,
):
    pipeline._fetch_articles = Mock(
        return_value=[]
    )

    pipeline._analyze_articles = Mock(
        return_value=[]
    )

    pipeline._export_results = Mock()

    pipeline.run()

    pipeline._fetch_articles.assert_called_once()

    pipeline._analyze_articles.assert_called_once_with(
        []
    )

    pipeline._export_results.assert_called_once_with(
        [],
        [],
    )

def test_run_propagates_fetch_exception(
    pipeline,
):
    pipeline._fetch_articles = Mock(
        side_effect=RuntimeError(
            "RSS Failure"
        )
    )

    with pytest.raises(
        RuntimeError
    ):
        pipeline.run()

def test_run_propagates_analysis_exception(
    pipeline,
):
    articles = [Mock()]

    pipeline._fetch_articles = Mock(
        return_value=articles
    )

    pipeline._analyze_articles = Mock(
        side_effect=RuntimeError(
            "Analysis Failure"
        )
    )

    with pytest.raises(
        RuntimeError
    ):
        pipeline.run()

