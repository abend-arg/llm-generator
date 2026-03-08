from domain import ExtractedContent, SourceType


class DefaultTitleExtractor:
    def extract(self, url: str) -> ExtractedContent:
        if not url:
            raise ValueError("missing url")
        return ExtractedContent(
            source_url=url,
            source_type=SourceType.DEFAULT,
            title=url,
            summary=None,
            info=None,
            sections=[],
        )
