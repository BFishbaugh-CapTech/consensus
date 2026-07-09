class LLMClientError(Exception):
    """Raised when communication with the LLM fails."""


class PromptGenerationError(Exception):
    """Raised when a prompt cannot be generated."""


class AnalysisParseError(Exception):
    """Raised when an LLM response cannot be parsed."""