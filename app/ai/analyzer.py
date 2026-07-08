from app.ai.llm_client import LLMClient
from app.models.analysis import Analysis
from app.models.article import Article


class Analyzer:
    """
    Responsible for analyzing a single news article.

    Coordinates prompt generation, LLM communication,
    and conversion into an Analysis object.
    """

    def __init__(
        self,
        client: LLMClient,
    ) -> None:
        self.client = client

    def analyze(
        self,
        article: Article,
    ) -> Analysis:
        """
        Analyze a single article.
        """

        prompt = self._build_prompt(article)

        response = self.client.generate(prompt)

        analysis = self._parse_response(
            article.id,
            response,
        )

        return analysis

    def _build_prompt(
        self,
        article: Article,
    ) -> str:
        """
        Build the prompt that will be sent to the LLM.
        """

        raise NotImplementedError

    def _parse_response(
        self,
        article_id: str,
        response: str,
    ) -> Analysis:
        """
        Convert the LLM response into an Analysis object.
        """

        raise NotImplementedError