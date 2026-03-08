from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExtractedContent:
    source_url: str
    source_type: str
    content: str
