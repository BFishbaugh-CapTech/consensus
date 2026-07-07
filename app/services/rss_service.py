import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import asdict

import feedparser

from app.models.article import Article


class RSSService:
    def __init__(self, config_path: str = "app/config/news_sources.json"):
        self.config_path = Path(config_path)

    def get_articles(self) -> list[Article]:
        """
        Fetch all configured RSS feeds and return a list of Articles.
        """
        articles = []

        sources = self._load_sources()

        for source in sources:
            try:
                articles.extend(self._fetch_feed(source))
            except Exception as e:
                print(f"Failed to fetch {source['name']}: {e}")

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

        # Timestamp when this feed was retrieved
        retrieved_at = datetime.now(timezone.utc)

        articles = []

        for entry in feed.entries:
            url = getattr(entry, "link", "")

            published = self._parse_datetime(
                getattr(entry, "published", None)
            )

            article = Article(
                id=self._generate_id(url),
                title=getattr(entry, "title", ""),
                url=url,
                published_at=published,
                retrieved_at=retrieved_at,
                source=source["name"],
                author=getattr(entry, "author", None),
                content="",
                summary=getattr(entry, "summary", None),
            )

            articles.append(article)

        return articles

    def export_articles_to_json(
        self,
        articles: list[Article],
        output_path: str = "data/articles.json",
    ) -> None:
        """
        Export a list of Article objects to a JSON file.
        """

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as file:
            json.dump(
                [asdict(article) for article in articles],
                file,
                indent=4,
                default=str,  # Converts datetime objects to strings
            )

        print(f"Exported {len(articles)} articles to {output}")    

    @staticmethod
    def _generate_id(url: str) -> str:
        """
        Generate a deterministic ID from the article URL.
        """
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    @staticmethod
    def _parse_datetime(date_string: str | None):
        """
        Convert an RSS published string into a datetime.
        Returns None if parsing fails.
        """
        if not date_string:
            return None

        try:
            return datetime.strptime(
                date_string,
                "%a, %d %b %Y %H:%M:%S %z",
            )
        except ValueError:
            return None