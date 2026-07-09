import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import asdict

import feedparser

from app.models.article import Article
from email.utils import parsedate_to_datetime
from app.config.settings import settings

logger = logging.getLogger(__name__)


class RSSService:
    def __init__(self, config_path: str = "app/config/news_sources.json"):
        self.config_path = Path(config_path)

    def get_articles(self) -> list[Article]:
        """
        Fetch all configured RSS feeds and return a list of Articles.
        """

        articles: list[Article] = []

        logger.info("- LOADING NEWS SOURCES -")

        sources = self._load_sources()

        logger.info(
            "LOADED %d NEWS SOURCES (MAX %d ARTICLES EACH):",
            len(sources),
            settings.MAX_ARTICLES_PER_SOURCE,
        )

        for source in sources:
            try:
                source_articles = self._fetch_feed(source)

                articles.extend(source_articles)

                logger.info(
                    "%-22s %3d articles",
                    source["name"],
                    len(source_articles),
                )

            except Exception:
                logger.exception(
                    "Failed to fetch feed: %s",
                    source["name"],
                )

        logger.info("-" * 35)
        logger.info("TOTAL ARTICLES: %d", len(articles))

        return articles

    def _load_sources(self) -> list[dict]:
        with open(self.config_path, "r", encoding="utf-8") as file:
            sources = json.load(file)

        return sources

    def _fetch_feed(self, source: dict) -> list[Article]:
        """
        Fetch a single RSS feed and convert its entries into Article objects.
        """

        feed = feedparser.parse(source["rss_url"])

        if feed.bozo:
            logger.warning(
                "%s returned a malformed RSS feed.",
                source["name"],
            )

        if not feed.entries:
            logger.warning(
                "%s returned no entries.",
                source["name"],
            )
            return []

        retrieved_at = datetime.now(timezone.utc)

        entries = feed.entries[
            : settings.MAX_ARTICLES_PER_SOURCE
        ]

        logger.debug(
            "Processing %d of %d available articles from %s.",
            len(entries),
            len(feed.entries),
            source["name"],
        )

        articles: list[Article] = []

        for entry in entries:
            try:
                article = self._populate_article(
                    source,
                    entry,
                    retrieved_at,
                )

                articles.append(article)

            except Exception:
                logger.exception(
                    "Failed to parse article from %s",
                    source["name"],
                )

        return articles

    def export_articles_to_json(
        self,
        articles: list[Article],
        output_path: str | None = None,
    ) -> None:
        """
        Export a list of Article objects to a JSON file.

        If no output path is provided, a filename is generated based on
        the current date and time of day.
        """

        if output_path is None:
            output_path = f"data/{self._generate_output_filename()}"

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as file:
            json.dump(
                [asdict(article) for article in articles],
                file,
                indent=4,
                default=str,
            )

        logger.info(
            "Exported %d articles to %s",
            len(articles),
            output,
        )

    @staticmethod
    def _generate_output_filename() -> str:
        """
        Generate a filename based on the current date and time.

        Morning   : Before 12:00 PM
        Afternoon : 12:00 PM - 4:59 PM
        Evening   : 5:00 PM and later

        Example:
            2026_07_08_MorningArticles.json
        """

        now = datetime.now()

        if now.hour < 12:
            period = "Morning"
        elif now.hour < 17:
            period = "Afternoon"
        else:
            period = "Evening"

        return f"{now:%Y_%m_%d}_{period}Articles.json"

    def _populate_article(
        self,
        source: dict,
        entry,
        retrieved_at: datetime,
    ) -> Article:
        """
        Convert one RSS entry into a normalized Article.
        """

        # Required fields
        title = getattr(entry, "title", "").strip()
        url = getattr(entry, "link", "").strip()

        # Optional fields
        author = getattr(entry, "author", None)

        summary = getattr(entry, "summary", None)
        if summary:
            summary = summary.strip()

        # Content (many RSS feeds don't include it)
        content = ""

        if hasattr(entry, "content") and entry.content:
            content = entry.content[0].get("value", "")
        elif hasattr(entry, "description"):
            content = entry.description

        if content:
            content = content.strip()

        return Article(
            id=self._generate_id(url),
            title=title,
            url=url,
            published_at=self._parse_datetime(
                getattr(entry, "published", None)
            ),
            retrieved_at=retrieved_at,
            source=source["name"],
            author=author,
            content=content,
            summary=summary,
        )

    @staticmethod
    def _generate_id(url: str) -> str:
        """
        Generate a deterministic ID from the article URL.
        """
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    @staticmethod
    def _parse_datetime(date_string: str | None) -> datetime | None:
        """
        Convert an RSS published date into a UTC datetime.

        Returns None if parsing fails.
        """

        if not date_string:
            return None

        try:
            return parsedate_to_datetime(date_string).astimezone(timezone.utc)
        except (TypeError, ValueError):
            return None