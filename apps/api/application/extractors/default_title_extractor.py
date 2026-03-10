from domain import ExtractedContent, ExtractionStrategy


class DefaultTitleExtractor:
    def extract(self, url: str) -> ExtractedContent:
        if not url:
            raise ValueError("missing url")
        return ExtractedContent(
            source_url=url,
            extraction_strategy=ExtractionStrategy.DEFAULT,
            title=url,
            summary=None,
            info=None,
            sections=[],
        )
