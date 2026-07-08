from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Analysis:
    """
    AI-generated analysis of a single news article.
    """

    # Relationships
    article_id: str
    story_id: Optional[str] = None

    # Topic Classification
    topics: list[str] = field(default_factory=list)

    # Named Entities
    people: list[str] = field(default_factory=list)
    organizations: list[str] = field(default_factory=list)
    locations: list[str] = field(default_factory=list)

    # Bias Analysis
    political_lean: Optional[str] = None
    bias_score: Optional[float] = None

    # Writing Style
    emotional_tone: Optional[str] = None

    # AI Confidence
    confidence: Optional[float] = None

    # AI Reasoning
    reasoning: Optional[str] = None