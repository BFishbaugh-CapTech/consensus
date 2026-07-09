import json
import logging

from app.ai.llm_client import LLMClient
from app.ai.exceptions import LLMClientError
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

            analysis = self._parse_response(
                article.id,
                response,
            )

            logger.info(
                "Successfully analyzed article %s",
                article.id,
            )

            return analysis

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
Return ONLY a valid JSON object.

The JSON object MUST:

- Match this schema exactly.
- Include every property.
- Never include markdown.
- Never include comments.
- Never include additional properties.
- Use null when a value cannot be determined.

{
    "headline": "",
    "primary_event": "",
    "topics": [
        "Example Topic"
    ],
    "people": [
        "Example People"
    ],
    "organizations": [
        "Example Organization"
    ],
    "locations": [
        "Example Location"
    ],
    "summary": "Example Summary",
    "political_lean": "Center",
    "bias_score": 0.0,
    "emotional_tone": "Neutral",
    "confidence": 0.0,
    "reasoning": "Example Reasoning"
}
""".strip()

    def _article(
        self,
        article: Article,
    ) -> str:
        """
        Format the article for the prompt.
        """

        summary = article.summary or "Not provided."

        content = article.content or "Not provided."

        return f"""
ARTICLE

Title:
{article.title}

Source:
{article.source}

Summary:
{summary}

Content:
{content}
""".strip()

    def _normalize_list(
        self,
        value,
    ) -> list[str]:
        """
        Normalize an LLM value into a list of strings.
        """

        if value is None:
            return []

        if isinstance(value, list):
            return [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

        if isinstance(value, str):
            value = value.strip()

            if not value:
                return []

            return [value]

        return [str(value)]

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

        logger.debug("Raw LLM Response:\n%s", response)

        try:
            data = json.loads(response)

        except json.JSONDecodeError as ex:
            raise LLMClientError(
                "LLM returned invalid JSON."
            ) from ex

        topics = sorted(
            set(
                self._normalize_list(
                    data.get("topics")
                )
            )
        )

        people = sorted(
            set(
                self._normalize_list(
                    data.get("people")
                )
            )
        )

        organizations = sorted(
            set(
                self._normalize_list(
                    data.get("organizations")
                )
            )
        )

        locations = sorted(
            set(
                self._normalize_list(
                    data.get("locations")
                )
            )
        )

        bias_score = data.get("bias_score")

        if (
            bias_score is not None
            and not isinstance(bias_score, (int, float))
        ):
            raise LLMClientError(
                "bias_score must be numeric."
            )

        if (
            bias_score is not None
            and not -1.0 <= bias_score <= 1.0
        ):
            raise LLMClientError(
                "bias_score must be between -1.0 and 1.0."
            )

        confidence = data.get("confidence")

        if (
            confidence is not None
            and not isinstance(confidence, (int, float))
        ):
            raise LLMClientError(
                "confidence must be numeric."
            )

        if (
            confidence is not None
            and not 0.0 <= confidence <= 1.0
        ):
            raise LLMClientError(
                "confidence must be between 0.0 and 1.0."
            )

        political_lean = data.get("political_lean")

        if political_lean:
            political_lean = political_lean.title()

        emotional_tone = data.get("emotional_tone")

        if emotional_tone:
            emotional_tone = emotional_tone.title()

        try:
            return Analysis(
                article_id=article_id,
                headline=data["headline"],
                primary_event=data["primary_event"],
                summary=data["summary"],
                topics=topics,
                people=people,
                organizations=organizations,
                locations=locations,
                political_lean=political_lean,
                bias_score=bias_score,
                emotional_tone=emotional_tone,
                confidence=confidence,
                reasoning=data.get("reasoning"),
            )

        except KeyError as ex:
            raise LLMClientError(
                f"Missing required field '{ex.args[0]}' in LLM response."
            ) from ex