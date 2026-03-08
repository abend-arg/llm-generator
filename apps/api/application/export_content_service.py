from fastapi import Depends

from .renderers import LlmsTxtRenderer, RendererProtocol


class ExportContentService:
    def __init__(self, renderer: RendererProtocol = Depends(LlmsTxtRenderer)) -> None:
        self._renderer = renderer

    def export(self, url: str) -> tuple[str, str]:
        return self._renderer.render(url)
