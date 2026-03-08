from fastapi import Depends

from .extractors import ExtractorSelector
from .renderers import LlmsTxtRenderer, RendererProtocol


class ExportContentService:
    def __init__(
        self,
        renderer: RendererProtocol = Depends(LlmsTxtRenderer),
        selector: ExtractorSelector = Depends(),
    ) -> None:
        self._renderer = renderer
        self._selector = selector

    def export(self, url: str) -> tuple[str, str]:
        extractor = self._selector.pick(url)
        data = extractor.extract(url)
        return self._renderer.render(data)
