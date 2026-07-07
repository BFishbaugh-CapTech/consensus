from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    id: str

    title: str
    url: str

    published_at: Optional[datetime]
    retrieved_at: datetime

    source: str
    author: Optional[str]

    content: str

    summary: Optional[str] = None