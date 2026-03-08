from domain import ExtractedContent, SourceType


class LlmsTxtExtractor:
    def extract(self, url: str) -> ExtractedContent:
        return ExtractedContent(source_url=url, source_type=SourceType.LLMS_TXT, content="")
