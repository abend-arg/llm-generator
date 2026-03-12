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
    max_paragraphs_per_page: int
    link_penalty_keywords: dict[str, int]

    @classmethod
    def default(cls) -> "CrawlerPolicies":
        return cls(
            max_pages=4,
            max_paragraphs_per_page=12,
            link_penalty_keywords={
                "support": -8,
                "faq": -8,
            },
        )
