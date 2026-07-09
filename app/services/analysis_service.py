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

    def export_analysis_to_json(
        self,
        analyses: list[Analysis],
        output_path: str | None = None,
    ) -> None:
        """
        Export Analysis objects to JSON.
        """

        if output_path is None:
            output_path = self._default_output_path()

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
                [asdict(analysis) for analysis in analyses],
                file,
                indent=4,
                default=str,
            )

        logger.info(
            "Exported %d analyses to %s",
            len(analyses),
            output,
        )

    def _default_output_path(
        self,
    ) -> str:
        """
        Generate the default output filename.
        """

        now = datetime.now()

        if now.hour < 12:
            period = "Morning"
        elif now.hour < 17:
            period = "Afternoon"
        else:
            period = "Evening"

        return (
            f"data/"
            f"{now:%Y_%m_%d}_"
            f"{period}"
            f"Analysis.json"
        )