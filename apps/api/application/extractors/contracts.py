from typing import Protocol

from domain import ExtractedContent


class ExtractorProtocol(Protocol):
    def extract(self, data: ExtractedContent) -> ExtractedContent: ...
