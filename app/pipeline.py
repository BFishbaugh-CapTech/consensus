import logging

from app.ai.analyzer import Analyzer
from app.ai.llm_client import LLMClient
from app.models.analysis import Analysis
from app.models.article import Article
from app.services.analysis_service import AnalysisService
from app.services.rss_service import RSSService

logger = logging.getLogger(__name__)


class Pipeline:
    """
    Coordinates the end-to-end Consensus pipeline.

        RSS Feeds
            ↓
        Articles
            ↓
        AI Analysis
            ↓
        JSON Output
    """

    def __init__(self) -> None:
        self.rss_service = RSSService()

        self.llm_client = LLMClient()

        self.analyzer = Analyzer(
            self.llm_client,
        )

        self.analysis_service = AnalysisService(
            self.analyzer,
        )

    def run(self) -> None:
        """
        Execute the full Consensus pipeline.
        """

        logger.info("=" * 60)
        logger.info("Starting Consensus Pipeline")
        logger.info("=" * 60)

        articles = self._fetch_articles()

        analyses = self._analyze_articles(
            articles,
        )

        self._export_results(
            articles,
            analyses,
        )

        logger.info("=" * 60)
        logger.info("Consensus Pipeline Complete")
        logger.info("=" * 60)

    def _fetch_articles(
        self,
    ) -> list[Article]:
        """
        Fetch all configured RSS feeds.
        """

        logger.info("Fetching articles...")

        articles = self.rss_service.get_articles()

        logger.info(
            "Fetched %d articles.",
            len(articles),
        )

        return articles

    def _analyze_articles(
        self,
        articles: list[Article],
    ) -> list[Analysis]:
        """
        Analyze every article.
        """

        logger.info("Analyzing articles...")

        analyses = self.analysis_service.analyze_articles(
            articles,
        )

        logger.info(
            "Generated %d analyses.",
            len(analyses),
        )

        return analyses

    def _export_results(
        self,
        articles: list[Article],
        analyses: list[Analysis],
    ) -> None:
        """
        Export articles and analyses to JSON.
        """

        logger.info("Exporting results...")

        self.rss_service.export_articles_to_json(
            articles,
        )

        self.analysis_service.export_analysis_to_json(
            analyses,
        )

        logger.info("Export complete.")