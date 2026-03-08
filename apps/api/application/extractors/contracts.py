from typing import Protocol

from domain import ExtractedContent


class ExtractorProtocol(Protocol):
    def extract(self, url: str) -> ExtractedContent: ...


class CouldNotExtract(Exception):
    """Raised when an extractor cannot extract data and should fall back."""
