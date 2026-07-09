import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from app.ai.analyzer import Analyzer
from app.models.analysis import Analysis
from app.models.article import Article

logger = logging.getLogger(__name__)


class AnalysisService:
    """
    Coordinates the analysis of a collection of Articles.
    """

    def __init__(
        self,
        analyzer: Analyzer,
    ) -> None:
        self.analyzer = analyzer

    def analyze_articles(
        self,
        articles: list[Article],
    ) -> list[Analysis]:
        """
        Analyze a collection of articles.
        """

        analyses: list[Analysis] = []

        logger.info(
            "Beginning analysis of %d articles.",
            len(articles),
        )

        for article in articles:
            try:
                analysis = self.analyzer.analyze(article)

                analyses.append(analysis)

                logger.info(
                    "Analyzed article: %s",
                    article.title,
                )

            except Exception:
                logger.exception(
                    "Failed to analyze article %s",
                    article.id,
                )

        logger.info(
            "Successfully analyzed %d of %d articles.",
            len(analyses),
            len(articles),
        )

        return analyses

    def load_articles(
        self,
        input_path: str,
    ) -> list[Article]:
        """
        Load Article objects from a JSON file.
        """

        with open(input_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        articles = [
            Article(
                id=item["id"],
                title=item["title"],
                url=item["url"],
                published_at=(
                    datetime.fromisoformat(item["published_at"])
                    if item["published_at"]
                    else None
                ),
                retrieved_at=datetime.fromisoformat(
                    item["retrieved_at"]
                ),
                source=item["source"],
                author=item["author"],
                content=item["content"],
                summary=item["summary"],
            )
            for item in data
        ]

        logger.info(
            "Loaded %d articles from %s",
            len(articles),
            input_path,
        )

        return articles

    def export_analysis_to_json(
        self,
        analyses: list[Analysis],
        output_path: str,
    ) -> None:
        """
        Export Analysis objects to JSON.
        """

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                [asdict(a) for a in analyses],
                file,
                indent=4,
            )

        logger.info(
            "Exported %d analyses to %s",
            len(analyses),
            output,
        )