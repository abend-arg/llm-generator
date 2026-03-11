import logging

from fastapi import Depends

from .extractors import CouldNotExtract, ExtractorProtocol
from .extractors.deps import get_extractors
from .renderers import LlmsTxtRenderer, RendererProtocol


class ExportContentService:
    _LOGGER = logging.getLogger(__name__)

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
                self._LOGGER.info(
                    "extractor_fallback extractor=%s", extractor.__class__.__name__
                )
                continue
            self._LOGGER.info(
                "extractor_selected strategy=%s", data.extraction_strategy.value
            )
            break
        return self._renderer.render(data)
