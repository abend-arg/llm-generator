from typing import Protocol


class RendererProtocol(Protocol):
    def render(self, url: str) -> tuple[str, str]: ...
