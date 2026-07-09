import json
import logging
import time
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

        total = len(articles)

        logger.info(
            "Beginning analysis of %d articles.",
            total,
        )

        start_time = time.perf_counter()

        for index, article in enumerate(
            articles,
            start=1,
        ):
            article_start = time.perf_counter()

            try:
                logger.info(
                    "[%d/%d] Analyzing (%s): %s",
                    index,
                    total,
                    article.source,
                    article.title,
                )

                analysis = self.analyzer.analyze(article)

                analyses.append(analysis)

                article_time = (
                    time.perf_counter() - article_start
                )

                elapsed = (
                    time.perf_counter() - start_time
                )

                average = elapsed / index
                remaining = average * (total - index)

                logger.info(
                    "[%d/%d] Complete (%.2fs) | ETA %.0fs",
                    index,
                    total,
                    article_time,
                    remaining,
                )

            except Exception:
                logger.exception(
                    "[%d/%d] Failed to analyze article %s",
                    index,
                    total,
                    article.id,
                )

        logger.info(
            "Successfully analyzed %d of %d articles.",
            len(analyses),
            total,
        )

        logger.info(
            "Analysis completed in %.2f seconds.",
            time.perf_counter() - start_time,
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