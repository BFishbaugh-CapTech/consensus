import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.exceptions.exceptions import LLMClientError

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
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
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
            "Generating response using model '%s'.",
            self.model,
        )

        logger.debug(
            "Prompt length: %d characters",
            len(prompt),
        )

        try:
            response = self.client.responses.create(
                **self._build_request(prompt)
            )

            text = response.output_text.strip()

            if not text:
                raise LLMClientError(
                    "LLM returned an empty response."
                )

            logger.info(
                "Successfully received response from '%s'.",
                self.model,
            )

            logger.debug(
                "Response length: %d characters",
                len(text),
            )

            return text

        except LLMClientError:
            raise

        except Exception as ex:
            logger.exception(
                "Failed to generate LLM response."
            )

            raise LLMClientError(
                "Unable to generate response."
            ) from ex

    def _build_request(
        self,
        prompt: str,
    ) -> dict:
        """
        Build the request sent to the OpenAI Responses API.
        """

        return {
            "model": self.model,
            "input": prompt,

            # -----------------------------------------------------------------
            # Future configuration options
            #
            # Uncomment or expand these as the project evolves.
            # -----------------------------------------------------------------

            # "temperature": 0.2,
            # "max_output_tokens": 2000,

            # Force JSON output (supported models / APIs)
            # "text": {
            #     "format": {
            #         "type": "json_object",
            #     }
            # },
        }