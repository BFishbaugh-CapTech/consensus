import json
import logging

from app.ai.llm_client import LLMClient
from app.exceptions.exceptions import LLMClientError
from app.models.analysis import Analysis
from app.models.article import Article

logger = logging.getLogger(__name__)


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

        try:
            prompt = self._build_prompt(article)

            response = self.client.generate(prompt)

            return self._parse_response(
                article.id,
                response,
            )

        except LLMClientError:
            logger.exception(
                "Failed to analyze article %s",
                article.id,
            )
            raise

        except Exception:
            logger.exception(
                "Unexpected error while analyzing article %s",
                article.id,
            )
            raise

    # ------------------------------------------------------------------
    # Prompt Construction
    # ------------------------------------------------------------------

    def _build_prompt(
        self,
        article: Article,
    ) -> str:
        """
        Build the prompt sent to the LLM.
        """

        return f"""
{self._system_prompt()}

{self._analysis_instructions()}

{self._json_schema()}

{self._example_response()}

{self._article(article)}
""".strip()

    def _system_prompt(self) -> str:
        """
        Define the AI's role.
        """

        return """
You are an impartial news analyst.

Your responsibility is to analyze a single news article objectively.

Treat the article as evidence, not truth.

Do not summarize opinions as facts.

Do not infer information that is not explicitly supported by the article.

If information cannot be determined from the article, return null instead of guessing.

Return ONLY valid JSON.

Do not include markdown.

Do not include any text outside of the JSON response.
""".strip()

    def _analysis_instructions(self) -> str:
        """
        Define the requested analysis.
        """

        return """
Analyze the supplied news article.

Produce the following information:

• headline
    - Neutral headline
    - Maximum 10 words

• primary_event
    - One sentence describing the underlying event

• topics
    - List of major news topics

• people
    - Important people

• organizations
    - Important organizations

• locations
    - Important locations

• summary
    - 100–200 word factual summary

• political_lean
    - Choose exactly one:
        Left
        Lean Left
        Center
        Lean Right
        Right
        Unknown

• bias_score
    - Decimal between -1.0 and 1.0

• emotional_tone
    - One descriptive word

• confidence
    - Decimal between 0.0 and 1.0

• reasoning
    - Explain why you selected the political leaning,
      bias score, and emotional tone.
""".strip()

    def _json_schema(self) -> str:
        """
        Define the required JSON schema.
        """

        return """
The JSON response MUST exactly match this schema.

{
    "headline": "",
    "primary_event": "",
    "topics": [],
    "people": [],
    "organizations": [],
    "locations": [],
    "summary": "",
    "political_lean": "",
    "bias_score": 0.0,
    "emotional_tone": "",
    "confidence": 0.0,
    "reasoning": ""
}

Do not omit fields.

Use null if a value cannot be determined.

Do not include additional properties.
""".strip()

    def _example_response(self) -> str:
        """
        Example JSON response.
        """

        return """
Example:

{
    "headline": "Congress Passes Budget Bill",
    "primary_event": "Congress approves a federal budget bill.",
    "topics": [
        "Politics",
        "Government"
    ],
    "people": [
        "Jane Doe"
    ],
    "organizations": [
        "United States Congress"
    ],
    "locations": [
        "United States"
    ],
    "summary": "Congress passed a federal budget bill after several weeks of negotiations between lawmakers. The legislation includes funding for government operations and several policy initiatives. Supporters argued that the bill provides economic stability, while opponents criticized portions of the spending package. The article presents the timeline of negotiations, reactions from elected officials, and expected next steps before implementation.",
    "political_lean": "Center",
    "bias_score": 0.03,
    "emotional_tone": "Neutral",
    "confidence": 0.96,
    "reasoning": "The article presents multiple viewpoints and uses predominantly factual language with limited emotionally charged wording."
}
""".strip()

    def _article(
        self,
        article: Article,
    ) -> str:
        """
        Format the article for the prompt.
        """

        return f"""
ARTICLE

Title:
{article.title}

Source:
{article.source}

Summary:
{article.summary}

Content:
{article.content}
""".strip()

    # ------------------------------------------------------------------
    # Response Parsing
    # ------------------------------------------------------------------

    def _parse_response(
        self,
        article_id: str,
        response: str,
    ) -> Analysis:
        """
        Convert the LLM response into an Analysis object.
        """

        try:
            data = json.loads(response)

        except json.JSONDecodeError as ex:
            raise LLMClientError(
                "LLM returned invalid JSON."
            ) from ex

        try:
            return Analysis(
                article_id=article_id,
                headline=data["headline"],
                primary_event=data["primary_event"],
                topics=data["topics"],
                people=data["people"],
                organizations=data["organizations"],
                locations=data["locations"],
                summary=data["summary"],
                political_lean=data.get("political_lean"),
                bias_score=data.get("bias_score"),
                emotional_tone=data.get("emotional_tone"),
                confidence=data.get("confidence"),
                reasoning=data.get("reasoning"),
            )

        except KeyError as ex:
            raise LLMClientError(
                f"Missing required field '{ex.args[0]}' in LLM response."
            ) from ex