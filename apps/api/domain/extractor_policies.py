from dataclasses import dataclass

from .models import ExtractionStrategy

EXTRACTOR_ORDER: list[ExtractionStrategy] = [
    ExtractionStrategy.LLMS_TXT,
    ExtractionStrategy.HTML,
    ExtractionStrategy.CRAWLER,
    ExtractionStrategy.DEFAULT,
]

@dataclass(frozen=True, slots=True)
class CrawlerPolicies:
    max_pages: int

    @classmethod
    def default(cls) -> "CrawlerPolicies":
        return cls(max_pages=4)
