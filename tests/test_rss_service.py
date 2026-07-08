from datetime import datetime, timezone
from unittest.mock import Mock, patch

from app.models.article import Article
from app.services.rss_service import RSSService
from pathlib import Path


def test_generate_id():
    url = "https://example.com/article"

    id1 = RSSService._generate_id(url)
    id2 = RSSService._generate_id(url)

    assert id1 == id2


def test_generate_id_different_urls():
    id1 = RSSService._generate_id("https://example.com/1")
    id2 = RSSService._generate_id("https://example.com/2")

    assert id1 != id2


def test_parse_datetime_valid():
    result = RSSService._parse_datetime(
        "Tue, 08 Jul 2026 10:00:00 GMT"
    )

    assert result is not None
    assert isinstance(result, datetime)


def test_parse_datetime_invalid():
    result = RSSService._parse_datetime("this is not a date")

    assert result is None


def test_parse_datetime_none():
    result = RSSService._parse_datetime(None)

    assert result is None


def test_populate_article():
    service = RSSService()

    source = {
        "name": "CNN",
        "rss_url": "https://example.com/rss",
    }

    entry = Mock()

    entry.title = "Test Article"
    entry.link = "https://example.com/article"
    entry.author = "John Doe"
    entry.summary = "Summary"
    entry.description = "Content"
    entry.published = "Tue, 08 Jul 2026 10:00:00 GMT"
    entry.content = []

    article = service._populate_article(
        source,
        entry,
        datetime.now(timezone.utc),
    )

    assert isinstance(article, Article)

    assert article.title == "Test Article"
    assert article.url == "https://example.com/article"
    assert article.author == "John Doe"
    assert article.summary == "Summary"
    assert article.content == "Content"
    assert article.source == "CNN"


@patch("app.services.rss_service.feedparser.parse")
def test_fetch_feed_empty(mock_parse):
    service = RSSService()

    mock_feed = Mock()
    mock_feed.entries = []
    mock_feed.bozo = False

    mock_parse.return_value = mock_feed

    source = {
        "name": "CNN",
        "rss_url": "https://example.com/rss",
    }

    articles = service._fetch_feed(source)

    assert articles == []


@patch("app.services.rss_service.feedparser.parse")
def test_fetch_feed_returns_articles(mock_parse):
    service = RSSService()

    entry = Mock()

    entry.title = "Test"
    entry.link = "https://example.com"
    entry.author = None
    entry.summary = "Summary"
    entry.description = "Content"
    entry.published = "Tue, 08 Jul 2026 10:00:00 GMT"
    entry.content = []

    mock_feed = Mock()
    mock_feed.entries = [entry]
    mock_feed.bozo = False

    mock_parse.return_value = mock_feed

    source = {
        "name": "CNN",
        "rss_url": "https://example.com/rss",
    }

    articles = service._fetch_feed(source)

    assert len(articles) == 1
    assert articles[0].title == "Test"


@patch.object(RSSService, "_load_sources")
@patch.object(RSSService, "_fetch_feed")
def test_get_articles(mock_fetch_feed, mock_load_sources):
    service = RSSService()

    mock_load_sources.return_value = [
        {
            "name": "CNN",
            "rss_url": "rss1",
        },
        {
            "name": "Fox",
            "rss_url": "rss2",
        },
    ]

    article = Article(
        id="1",
        title="Test",
        url="https://example.com",
        published_at=None,
        retrieved_at=datetime.now(timezone.utc),
        source="CNN",
        author=None,
        content="",
        summary="",
    )

    mock_fetch_feed.return_value = [article]

    articles = service.get_articles()

    assert len(articles) == 2
    assert mock_fetch_feed.call_count == 2

def test_generate_output_filename():
    filename = RSSService._generate_output_filename()

    assert filename.endswith(".json")

    assert (
        "MorningArticles" in filename
        or "AfternoonArticles" in filename
        or "EveningArticles" in filename
    )

    parts = filename.split("_")

    assert len(parts) >= 4

def test_export_articles_to_json(tmp_path):
    service = RSSService()

    article = Article(
        id="1",
        title="Test",
        url="https://example.com",
        published_at=None,
        retrieved_at=datetime.now(timezone.utc),
        source="CNN",
        author=None,
        content="Content",
        summary="Summary",
    )

    output_file = tmp_path / "articles.json"

    service.export_articles_to_json(
        [article],
        str(output_file),
    )

    assert output_file.exists()

    contents = output_file.read_text()

    assert "Test" in contents
    assert "CNN" in contents