from dataclasses import dataclass
from enum import Enum


class SourceType(str, Enum):
    LLMS_TXT = "llms_txt"
    HTML = "html"


@dataclass(frozen=True, slots=True)
class ExtractedContent:
    source_url: str
    source_type: SourceType
    content: str
