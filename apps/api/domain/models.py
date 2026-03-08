from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True, slots=True)
class LinkItem:
    name: str
    url: str
    notes: str | None = None


@dataclass(frozen=True, slots=True)
class FileSection:
    title: str
    items: list[LinkItem] = field(default_factory=list)


class SourceType(str, Enum):
    LLMS_TXT = "llms_txt"
    HTML = "html"


@dataclass(frozen=True, slots=True)
class ExtractedContent:
    source_url: str
    source_type: SourceType
    title: str
    summary: str | None = None
    info: str | None = None
    sections: list[FileSection] = field(default_factory=list)
