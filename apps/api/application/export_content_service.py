from fastapi import Depends

from domain import ExtractedContent, SourceType
from .extractors import ExtractorProtocol
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
        data = ExtractedContent(
            source_url=url,
            source_type=SourceType.HTML,
            title=url,
            summary=None,
            info=None,
            sections=[],
        )
        for extractor in self._extractors:
            data = extractor.extract(data)
        return self._renderer.render(data)
