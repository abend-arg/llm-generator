from typing import Protocol

from domain import ExtractedContent


class RendererProtocol(Protocol):
    def render(self, data: ExtractedContent) -> tuple[str, str]: ...
