from fastapi import Depends

from domain import ExtractedContent, SourceType

from .extractors import CouldNotExtract, ExtractorProtocol
from .extractors.deps import get_extractors
from .renderers import LlmsTxtRenderer, RendererProtocol


class ExportContentService:
    def __init__(
        self,
        renderer: RendererProtocol = Depends(LlmsTxtRenderer),
        extractors: list[ExtractorProtocol] = Depends(get_extractors),
    ) -> None:
        self._renderer = renderer
        self._extractors = extractors

    def export(self, url: str) -> tuple[str, str]:
        for extractor in self._extractors:
            try:
                data = extractor.extract(url)
            except CouldNotExtract:
                continue
            break
        return self._renderer.render(data)
