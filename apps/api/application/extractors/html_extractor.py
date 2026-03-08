from domain import ExtractedContent, SourceType


class HtmlExtractor:
    def extract(self, url: str) -> ExtractedContent:
        return ExtractedContent(source_url=url, source_type=SourceType.HTML, content="")
