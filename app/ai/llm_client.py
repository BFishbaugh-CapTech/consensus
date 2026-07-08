import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.ai.exceptions import LLMClientError

logger = logging.getLogger(__name__)

load_dotenv()


class LLMClient:
    """
    Generic client responsible for communicating with a Large Language Model.

    This class intentionally knows nothing about Articles, Analysis,
    Stories, or Consensus. It only sends prompts and returns responses.
    """

    def __init__(
        self,
        model: str | None = None,
    ) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY was not found. "
                "Check your .env file."
            )

        self.client = OpenAI(api_key=api_key)

        self.model = (
            model
            or os.getenv("OPENAI_MODEL")
            or "gpt-5"
        )

        logger.info(
            "Initialized LLMClient (model=%s)",
            self.model,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to the configured LLM and return the response.
        """

        logger.info(
            "Sending prompt to model '%s'.",
            self.model,
        )

        logger.debug(
            "Prompt length: %d characters",
            len(prompt),
        )

        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
            )

            logger.info(
                "Successfully received response from '%s'.",
                self.model,
            )

            return response.output_text.strip()

        except Exception as ex:
            logger.exception(
                "Failed to generate LLM response."
            )

            raise LLMClientError(
                "Unable to generate response."
            ) from ex